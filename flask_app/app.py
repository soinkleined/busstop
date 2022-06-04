'''
https://github.com/realpython/flask-boilerplate
'''
import json
from flask import Flask, render_template, jsonify
import logging
from logging import Formatter, FileHandler
import threading
import time
from turbo_flask import Turbo
from busstop import getStops

update_interval=15

app = Flask(__name__)
turbo = Turbo(app)

@app.context_processor
def get_all_stops():
    all_stops=getStops()
    return dict(all_stops=all_stops)

@app.route("/")
def index():
    all_stops=getStops()
    return render_template("index.html")

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_stops).start()

def update_stops():
    with app.app_context():
        while True:
            time.sleep(update_interval)
            turbo.push(turbo.replace(render_template('busstop.html'), 'all_stops'))

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('started a python application server.')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
