from app.app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.info('info的log')
    logging.debug('debug的log')

    app.run(debug=True)
