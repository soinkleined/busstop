'''
https://github.com/realpython/flask-boilerplate
'''
import logging
from logging import Formatter, FileHandler
import threading
import time
from flask import Flask, render_template
from turbo_flask import Turbo
from busstop import get_stops

UPDATE_INTERVAL=15

app = Flask(__name__)
turbo = Turbo(app)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.context_processor
def get_all_stops():
    '''get all stops'''
    all_stops=get_stops()
    return dict(all_stops=all_stops)

@app.route("/")
def index():
    '''render index template'''
    return render_template("index.html")

@app.before_first_request
def before_first_request():
    '''start getting stops'''
    threading.Thread(target=update_stops).start()

def update_stops():
    '''update stops'''
    with app.app_context():
        while True:
            time.sleep(UPDATE_INTERVAL)
            turbo.push(turbo.replace(render_template('busstop.html'), 'all_stops'))

@app.errorhandler(500)
def internal_error(error):
    '''render 500 page'''
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    '''render 404 page'''
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Started busstop.')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
