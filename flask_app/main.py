"""
https://github.com/realpython/flask-boilerplate
"""
import logging
from logging import Formatter, FileHandler
import threading
import time
from flask import Flask, request, render_template
from turbo_flask import Turbo
from busstop import get_stops

UPDATE_INTERVAL = 15

app = Flask(__name__)
turbo = Turbo(app)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def update_stops():
    """update stops"""
    with app.app_context():
        while True:
            time.sleep(UPDATE_INTERVAL)
            turbo.push(turbo.replace(render_template('busstop.html'),
                                     'all_stops'))


@app.context_processor
def get_all_stops():
    """start getting stops"""
    all_stops = get_stops()
    return {"all_stops": all_stops}


@app.route("/")
def index():
    """render index template"""
    return render_template("index.html")


@app.route("/admin")
def admin():
    """render admin template"""
    with open('config.ini', 'r') as file:
        config_data = file.read()
    return render_template('admin.html', config_data=config_data)


@app.route("/admin", methods=['POST'])
def admin_post():
    """render admin post template"""
    config_data = request.form['config_data']
    if request.method == 'POST':
        with open('config.ini', 'w') as f:
            f.write(str(config_data))
    return render_template('admin.html', nopol=config_data)


@app.route("/about")
def about():
    """render about template"""
    return render_template("about.html")


@app.errorhandler(500)
def internal_error(error):
    """render 500 page"""
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    """render 404 page"""
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('/tmp/error.log')
    file_handler.setFormatter(
        Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s: %(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Started busstop.')

thread = threading.Thread(target=update_stops)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
