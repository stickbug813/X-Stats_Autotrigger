from dataclasses import dataclass, field
from typing import Dict
import yaml

@dataclass
class XPressionCfg:
    host: str
    port: int = 7788

@dataclass
class PlayerCfg:
    auto_takeoff_seconds: int = 6
    focus_mode: str = "on_take"  # on_take | before_take | off

@dataclass
class TeamBurstCfg:
    enabled: bool = True
    delay_after_player_seconds: float = 1.5
    auto_takeoff_seconds: int = 6
    thresholds: Dict[str, int] = field(default_factory=lambda: {
        "3PTR": 3, "2PTR": 3, "FT": 3
    })
    take_ids: Dict[str, Dict[str, int]] = field(default_factory=dict)

@dataclass
class TypesCfg:
    aliases: Dict[str, str] = field(default_factory=dict)
    player_enabled: Dict[str, bool] = field(default_factory=dict)
    bursts_enabled: Dict[str, bool] = field(default_factory=dict)

@dataclass
class AppCfg:
    stats_xml: str
    xpression: XPressionCfg
    logging_level: str = "INFO"
    debounce_ms: int = 400
    min_trigger_interval_ms: int = 0
    player: PlayerCfg = field(default_factory=PlayerCfg)
    team_bursts: TeamBurstCfg = field(default_factory=TeamBurstCfg)
    types: TypesCfg = field(default_factory=TypesCfg)

def load_config(path: str) -> AppCfg:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return AppCfg(
        stats_xml=raw["stats_xml"],
        xpression=XPressionCfg(**raw["xpression"]),
        logging_level=raw.get("logging_level", "INFO"),
        debounce_ms=raw.get("debounce_ms", 400),
        min_trigger_interval_ms=raw.get("min_trigger_interval_ms", 0),
        player=PlayerCfg(**raw.get("player", {})),
        team_bursts=TeamBurstCfg(**raw.get("team_bursts", {})),
        types=TypesCfg(**raw.get("types", {})),
    )
