from flask import Flask
from flask.ext.restful import Api
from flask_sqlalchemy import SQLAlchemy

from database import db
from resources import AssetResource
from resources import AssetCollectionResource
from resources import CreditResource
from resources import CreditCollectionResource
from resources import AssetCreditAssociationResource
from resources import CreditAssetAssociationResource

# TODOs
# deploy/install/tests/documentation
# drop tables for tests?
# frontend?
# find all the in code todos


def build_endpoints(api):
    '''
    Could be used to do all kinds of crazy routing
    when this gets long usually best to start using
    flask blue prints
    granted using flask-restful is already probably overkill
    endpoints are created by the meathods of the classes in
    resources.py
    '''
    api.add_resource(AssetResource, '/assets/<int:asset_id>')
    api.add_resource(AssetCollectionResource, '/assets')

    api.add_resource(CreditResource, '/credits/<int:credit_id>')
    api.add_resource(CreditCollectionResource, '/credits')

    api.add_resource(AssetCreditAssociationResource,
                     '/assets/<int:asset_id>/credits',
                     '/assets/<int:asset_id>/credits/<int:credit_id>')

    api.add_resource(CreditAssetAssociationResource,
                     '/credits/<int:credit_id>/assets')


def setup_flask(drop_all=False):
    '''
    initialize top level objects
    give orm and router accesss flash
    returns app and api to simplify
    usining this independently of the full app
    '''
    # TODO error handling
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        if drop_all:
            db.drop_all()
        db.create_all()
    api = Api(app, catch_all_404s=True)
    build_endpoints(api)
    return app, api


app, api = setup_flask(drop_all=True)


if __name__ == '__main__':
    # debug will only be true if launched by running this file
    # if you through uwsgi it will not use this mode by default
    app.run(debug=True, host='0.0.0.0', port=8000)
