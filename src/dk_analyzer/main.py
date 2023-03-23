import statistics
from typing import Any

import matplotlib.pyplot as plt
import requests
import typer

app = typer.Typer()

import requests

data = {"grant_type": "client_credentials"}


class Event:
    def __init__(self, event: dict[str, Any]) -> None:
        self._event = event
        self.current_hp = int(event["hitPoints"])
        self.max_hp = int(event["maxHitPoints"])
        self.heal_amount = int(event["amount"])

    def hp_percent(self) -> float:
        return (self.current_hp / self.max_hp) * 100

    def rp(self) -> float:
        # TODO weird error with > 100 RP in rare cases
        return min(int(self._event["classResources"][0]["amount"]) / 10, 100)

    def is_cast_by_player(self) -> bool:
        return self._event["classResources"][0]["max"] != 0


@app.command()
def analyze_ds_usage(
    report_id: str = typer.Option("jbapg7M32FTn16Rd"),
    fight_id: int = typer.Option(1),
    client_id: str = typer.Argument(..., envvar="CLIENT_ID"),
    client_secret: str = typer.Argument(..., envvar="CLIENT_SECRET"),
) -> None:
    token = get_access_token(client_id, client_secret)
    events = fetch_report(report_id=report_id, fight_id=fight_id, access_token=token["access_token"])
    plot_graph(events)


def plot_graph(events: list[Event]) -> None:
    hp_list: list[float] = []
    rp_list: list[float] = []
    for event in events:
        if not event.is_cast_by_player():
            continue
        hp_list.append(event.hp_percent())
        rp_list.append(event.rp())

    plt.grid(zorder=-1.0)
    plt.scatter(
        x=rp_list,
        y=hp_list,
        marker="o",
        zorder=4.0,
    )
    plt.xlabel("RP")
    plt.ylabel("HP%")
    add_visual_aid()
    add_title(hp_list, rp_list)
    plt.show()


def add_visual_aid():
    plt.vlines(95, ymin=0, ymax=100, colors="#FE2A17", linewidth=3.0, zorder=3.0, label="95 RP")
    plt.hlines(70, xmin=35, xmax=95, colors="#FEBD0D", linewidth=3.0, zorder=2.0, label="70% HP")
    plt.fill_between([35, 95], 70, 100, color="black", alpha=0.1)


def add_title(hp_list: list[float], rp_list: list[float]) -> None:
    mean_rp = statistics.mean(rp_list)
    mean_hp = statistics.mean(hp_list)
    plt.title(f"DS Usage (mean RP: {round(mean_rp)}, mean HP: {round(mean_hp)}%)")


def get_access_token(client_id: str, client_secret: str) -> dict[str, Any]:
    response = requests.post(
        "https://www.warcraftlogs.com/oauth/token",
        data=data,
        auth=(client_id, client_secret),
    )
    return response.json()


def fetch_report(report_id: str, fight_id: int, access_token: str) -> list[Event]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = f"""
query {{
	reportData {{
		report(code:"{report_id}"){{
			events(fightIDs:{fight_id},abilityID:45470,sourceClass:"DEATHKNIGHT",dataType:Healing,includeResources:true,limit:9000) {{
				data
				nextPageTimestamp
			}}
		}}
	}}
}}
    """
    response = requests.post(
        "https://www.warcraftlogs.com/api/v2/client",
        headers=headers,
        json={"query": body},
        params={"code": report_id},
    )
    json_events = response.json()["data"]["reportData"]["report"]["events"]["data"]
    return [Event(json_event) for json_event in json_events]


if __name__ == "__main__":
    app()
