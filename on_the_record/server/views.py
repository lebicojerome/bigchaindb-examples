"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation in Apiary:
 - http://docs.bigchaindb.apiary.io/
"""

import flask
from flask import current_app, request, Blueprint, render_template

import bigchaindb
from bigchaindb import util

from bigchaindb_common.python import assets, accounts

app_name = __name__.split('.')[0]
bigchain = bigchaindb.Bigchain()

basic_views = Blueprint('basic_views', __name__)
api_views = Blueprint('api_views', __name__)


@basic_views.route('/')
def index():
    return render_template('index.html')


@api_views.route('/accounts/')
def get_accounts():
    result = accounts.retrieve_accounts(app_name, bigchain)
    return flask.jsonify({'accounts': result})


@api_views.route('/accounts/', methods=['POST'])
def post_account():
    json_payload = request.get_json(force=True)
    tx = assets.create_asset(bigchain=bigchain,
                             to=json_payload['to'],
                             payload={'content': json_payload['content']})
    return flask.jsonify(**tx)


@api_views.route('/accounts/<account_vk>/assets/')
def get_assets_for_account(account_vk):
    result = assets.get_owned_assets(bigchain, account_vk)
    return flask.jsonify({'assets': result})


@api_views.route('/assets/', methods=['POST'])
def post_asset():
    json_payload = request.get_json(force=True)

    tx = assets.create_asset(bigchain=bigchain,
                             to=json_payload['to'],
                             payload={'content': json_payload['content']})

    return flask.jsonify(**tx)