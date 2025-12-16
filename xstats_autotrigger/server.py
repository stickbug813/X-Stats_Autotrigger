from flask import Flask, jsonify, request
from xstats_autotrigger.engine import compose_player_takeid


def build_app(cfg, rt, state, watcher):
    app = Flask(__name__)

    @app.route("/enable", methods=["PUT"])
    def enable():
        state.enabled = True
        return jsonify(ok=True)

    @app.route("/disable", methods=["PUT"])
    def disable():
        state.enabled = False
        return jsonify(ok=True)

    @app.route("/force_on", methods=["POST"])
    def force_on():
        data = request.get_json(force=True)
        take_id = compose_player_takeid(
            data["vh"],
            data["type"],
            data["uni"]
        )
        rt.send(f"SEQI {take_id}")
        return jsonify(ok=True)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify(
            enabled=state.enabled,
            xpression_ok=rt.healthy(),
            burst_counts=state.burst_counts,
            last_player_trigger_at=state.last_player_trigger_at
        )

    return app
