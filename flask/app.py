import argparse
import logging

from pathlib import PurePath, Path
from flask import Flask
from logging.config import fileConfig
from flask_restplus import Api
from waitress import serve

from api.product import api as api_products
from data import db

_logger = logging.getLogger()

parser = argparse.ArgumentParser('Database connection variables')
parser.add_argument('--db_user', type=str, default='docker')
parser.add_argument('--db_password', type=str, default='password')
parser.add_argument('--db_name', type=str, default='flask')
parser.add_argument('--db_host', type=str, default='localhost')
parser.add_argument('--db_port', type=str, default='5432')


class App(object):

    def __init__(self):
        self.api = Api(
            version='1.0',
            prefix='/api/v1',
            doc='/swagger',
            title='Todo API',
            description='A simple TODO API'
        )

    def logger_init(self) -> None:
        path = PurePath.joinpath(Path.cwd(), "logging_config.ini")
        fileConfig(path)
        _logger.info(f'logger initialized with config: {path}')


    def create_app(self, params: object) -> Flask:
        app = Flask(__name__)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        url = f"postgresql://{params.db_user}:{params.db_password}@{params.db_host}:{params.db_port}/{params.db_name}"
        app.config['SQLALCHEMY_DATABASE_URI'] = url
        self.register_extensions(app)
        self.register_api(app)
        _logger.info(f'app created')
        return app

    def register_extensions(self, app_definition: Flask) -> None:
        db.init_app(app_definition)

    def register_api(self, app_definition: Flask) -> None:
        self.api.add_namespace(api_products)
        self.api.init_app(app_definition)

    def setup_database(self, app_definition: Flask) -> None:
        with app_definition.app_context():
            db.create_all()


if __name__ == '__main__':
    main = App()
    args = parser.parse_args()
    main.logger_init()
    app = main.create_app(args)
    main.setup_database(app)
    serve(app, listen='0.0.0.0:5000')
