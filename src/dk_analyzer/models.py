from typing import Any


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
