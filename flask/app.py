import logging
import os

from pathlib import PurePath
from flask import Flask
from logging.config import fileConfig
from flask_restplus import Api

from api.product import api as api_products
from data import db

_logger = logging.getLogger()


class App(object):

    def __init__(self):
        self.db_user = os.getenv('DB_USER', 'docker')
        self.db_password = os.getenv('DB_PASSWORD', 'password')
        self.db_name = os.getenv('DB_NAME', 'postgres')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.api = Api(
            version='1.0',
            prefix='/api/v1',
            doc='/swagger',
            title='Product API',
            description='A simple product api'
        )

    def logger_init(self) -> None:
        path = PurePath.joinpath(PurePath(__file__).parent, 'logging_config.ini')
        fileConfig(path)
        _logger.info(f'logger initialized with config: {path}')

    def create_app(self) -> Flask:
        flask_app = Flask(__name__)
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        url = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = url
        self.register_extensions(flask_app)
        self.register_api(flask_app)
        _logger.info(f'app created')
        return flask_app

    def register_extensions(self, app_definition: Flask) -> None:
        db.init_app(app_definition)

    def register_api(self, app_definition: Flask) -> None:
        self.api.add_namespace(api_products)
        self.api.init_app(app_definition)

    def setup_database(self, app_definition: Flask) -> None:
        with app_definition.app_context():
            db.create_all()


main = App()
main.logger_init()
app = main.create_app()
main.setup_database(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
