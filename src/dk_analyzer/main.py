import typer

from dk_analyzer.graph_plotter import plot_graph
from dk_analyzer.warcraftlogs import fetch_report
from dk_analyzer.warcraftlogs import get_access_token

app = typer.Typer()


@app.command()
def analyze_ds_usage(
    report_id: str = typer.Option("jbapg7M32FTn16Rd"),
    fight_id: int = typer.Option(1),
    client_id: str = typer.Argument(..., envvar="CLIENT_ID"),
    client_secret: str = typer.Argument(..., envvar="CLIENT_SECRET"),
) -> None:
    events = fetch_report(
        report_id=report_id,
        fight_id=fight_id,
        access_token=get_access_token(client_id, client_secret),
    )
    plot_graph(events)


if __name__ == "__main__":
    app()
