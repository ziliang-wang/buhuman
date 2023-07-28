from flask import render_template

from app.app import create_app
import logging

app = create_app()


@app.errorhandler(404)
def not_found(err):
    return render_template('error.html')


@app.errorhandler(500)
def server_err(err):
    return render_template('error.html')


if __name__ == '__main__':
    logging.info('info的log')
    logging.debug('debug的log')

    app.run(debug=True)

