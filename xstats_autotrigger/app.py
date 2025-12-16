import argparse, logging
from xstats_autotrigger.config_loader import load_config
from xstats_autotrigger.engine import EngineState
from xstats_autotrigger.rosstalk import RossTalkClient
from xstats_autotrigger.watcher import XMLWatcher
from xstats_autotrigger.server import build_app

def main():
    parser = argparse.ArgumentParser(description="XSAT Auto Trigger v4.2")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    logging.basicConfig(level=cfg.logging_level)

    rt = RossTalkClient(cfg.xpression.host, cfg.xpression.port)
    state = EngineState()
    watcher = XMLWatcher(cfg, rt, state)
    watcher.start()

    app = build_app(cfg, rt, state, watcher)
    app.run(port=5005)

if __name__ == "__main__":
    main()
