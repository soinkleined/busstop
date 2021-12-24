'''
https://github.com/realpython/flask-boilerplate
'''
import json
from flask import Flask, render_template, jsonify
import logging
from logging import Formatter, FileHandler
from busstop import getStops


app = Flask(__name__)

@app.route("/")
def home():
    all_stops=getStops()
    return render_template("busstop.html", all_stops=all_stops)

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
    app.logger.info('errors')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
