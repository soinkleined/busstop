"""
Realtime London bus stop info via TFL.
https://github.com/soinkleined/busstop
"""

import logging
import threading
import time
from flask import Flask, redirect, request, render_template, url_for
from turbo_flask import Turbo
from tfl_bus_monitor.tfl_bus_monitor import TFLBusMonitor, get_config_path

UPDATE_INTERVAL = 15

app = Flask(__name__)
turbo = Turbo(app)
monitor = TFLBusMonitor()

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.propagate = False  # Prevent duplicate logging


def update_stops():
    """Push updates to client every UPDATE_INTERVAL seconds."""
    with app.app_context():
        while True:
            time.sleep(UPDATE_INTERVAL)
            turbo.push(
                turbo.replace(
                    render_template("busstop.html"),
                    target="all_stops"
                )
            )


@app.context_processor
def get_all_stops():
    """Inject stop data into templates."""
    return {"all_stops": monitor.get_all_arrivals()}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """View and update stop configuration."""
    if request.method == "POST":
        config_data = request.form["config_data"]
        with open(get_config_path(), "w") as f:
            f.write(config_data)
        return redirect(url_for("index"))
    else:
        with open(get_config_path(), "r") as f:
            config_data = f.read()
        return render_template("admin.html", config_data=config_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/stopinfo")
def stopinfo():
    return render_template("stopinfo.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


# Start the live update thread
thread = threading.Thread(target=update_stops)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    app.logger.info("busstop started")

