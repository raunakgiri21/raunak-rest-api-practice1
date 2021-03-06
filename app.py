import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.items import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True

uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key = 'raunak'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)