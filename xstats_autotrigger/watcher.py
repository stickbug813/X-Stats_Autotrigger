import time, os, threading, logging, xml.etree.ElementTree as ET
from xstats_autotrigger.engine import compose_player_takeid
from xstats_autotrigger.engine import EngineState

class XMLWatcher(threading.Thread):
    def __init__(self, cfg, rt, state: EngineState):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.rt = rt
        self.state = state
        self.aliases = {k.upper(): v.upper() for k, v in cfg.types.aliases.items()}
        self.player_enabled = cfg.types.player_enabled
        self.bursts_enabled = cfg.types.bursts_enabled

    def run(self):
        logging.info("XML Watcher Started: %s", self.cfg.stats_xml)
        while True:
            time.sleep(0.25)
            if not self.state.enabled:
                continue

            try:
                if os.path.getsize(self.cfg.stats_xml) == 0:
                    continue

                with open(self.cfg.stats_xml, "rb") as f:
                    root = ET.fromstring(f.read())

                plays = root.findall(".//play")

                if not self.state.first_parse_done:
                    for p in plays:
                        self.state.processed_keys.add(self._key(p))
                    self.state.first_parse_done = True
                    continue

                for p in plays:
                    self._handle_play(p)

            except Exception as e:
                logging.debug("XML parse skip: %s", e)

    def _key(self, p):
        return (
            p.get("vh"),
            self._canon(p.get("type")),
            p.get("uni"),
            p.get("action"),
            p.get("hscore"),
            p.get("vscore"),
        )

    def _canon(self, raw):
        raw = (raw or "").upper()
        return self.aliases.get(raw, raw)

    def _handle_play(self, p):
        key = self._key(p)
        if key in self.state.processed_keys:
            return
        self.state.processed_keys.add(key)

        stat = self._canon(p.get("type"))
        vh = p.get("vh")
        uni = p.get("uni")
        side = "home" if vh == "H" else "away"

        now = time.time()

        if self.player_enabled.get(stat, True):
            take = compose_player_takeid(vh, stat, uni)
            self.rt.send(f"SEQI {take}")
            self.rt.send(f"FOCUS {take}")
            threading.Timer(
                self.cfg.player.auto_takeoff_seconds,
                lambda: self.rt.send(f"SEQO {take}")
            ).start()
            self.state.last_player_trigger_at = now

        if self.cfg.team_bursts.enabled and self.bursts_enabled.get(stat, True):

            if stat not in self.cfg.team_bursts.thresholds:
                return

            self.state.burst_counts[side][stat] += 1

            if self.state.burst_counts[side][stat] >= self.cfg.team_bursts.thresholds[stat]:
                self.state.burst_counts[side][stat] = 0
                delay = (
                    self.cfg.player.auto_takeoff_seconds
                    + self.cfg.team_bursts.delay_after_player_seconds
                )
                threading.Timer(delay, lambda: self._fire_burst(side, stat)).start()

    def _fire_burst(self, side, stat):
        take = self.cfg.team_bursts.take_ids[side][stat]
        self.rt.send(f"SEQI {take}")
        threading.Timer(
            self.cfg.team_bursts.auto_takeoff_seconds,
            lambda: self.rt.send(f"SEQO {take}")
        ).start()