'''
Resources for the most part map to a combination of viewer and controller
in a mvc framework as it is now normally talked about
but they are closer to a model in the traditional GUI model of mvc
'''

from flask.ext.restful import Resource
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from flask.ext.restful import marshal_with
from sqlalchemy import desc
from sqlalchemy import text

from models import Asset
from models import Credit
from models import insert_credit_asset_association


credit_resource_fields = {'job_type': fields.String,
                          'name': fields.String, }


asset_resource_fields = {'title': fields.String,
                         'description': fields.String,
                         'thumbnail_url': fields.String,
                         'creation_date': fields.DateTime(dt_format='rfc822'), }


class CreditResource(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('name', required=True)
        self.post_reqparse.add_argument('job_type', required=True)
        self.put_reqparse = reqparse.RequestParser()
        self.put_reqparse.add_argument('name')
        self.put_reqparse.add_argument('job_type')

    @marshal_with(credit_resource_fields)
    def post(self):
        args = self.post_reqparse.parse_args()
        credit = Credit(args['job_type'], args['name'])
        # todo not putting location in header
        return credit, 201, {'location': '/asset/' + str(credit.identifier)}

    @marshal_with(credit_resource_fields)
    def put(self, credit_id):
        args = self.put_reqparse.parse_args()
        credit = Credit.query.filter_by(identifier=credit_id).first()
        if credit is None:
            credit = Credit(args['name'], args['job_type'])
            # todo not putting location in header
            return credit, 201
        credit.update(args['name'], args['job_type'])
        return credit, 200

    def delete(self, credit_id):
        credit = Credit.query.filter_by(identifier=credit_id).first()
        if credit is None:
            return '', 404
        credit.delete()
        return '', 204

    @marshal_with(credit_resource_fields)
    def get(self, credit_id):
        credit = Credit.query.filter_by(identifier=credit_id).first()
        return credit, 200


class AssetResource(Resource):
    def __init__(self):
        self.post_reqparse = reqparse.RequestParser()
        self.put_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('title', required=True)
        self.post_reqparse.add_argument('description', required=True)
        # TODO validate
        self.post_reqparse.add_argument('thumbnail_url', required=True)
        self.put_reqparse.add_argument('title')
        self.put_reqparse.add_argument('description')
        # TODO validate
        self.put_reqparse.add_argument('thumbnail_url')

    @marshal_with(asset_resource_fields)
    def post(self):
        args = self.post_reqparse.parse_args()
        asset = Asset(args['title'],
                      args['description'],
                      args['thumbnail_url'])
        header = {'location': '/asset/' + str(asset.identifier)}
        return asset, 201, header

    @marshal_with(asset_resource_fields)
    def put(self, asset_id):
        args = self.put_reqparse.parse_args()
        asset = Asset.query.filter_by(identifier=asset_id).first()
        if asset is None:
            asset = Asset(args['title'],
                          args['description'],
                          args['thumbnail_url'])
            header = {'location': '/asset/' + str(asset.identifier)}
            return asset, 201, header
        asset.update(args['title'], args['description'], args['thumbnail_url'])
        return asset, 200

    def delete(self, asset_id):
        asset = Asset.query.filter_by(identifier=asset_id).first()
        if asset is None:
            return '', 404
        asset.delete()
        return '', 204

    @marshal_with(asset_resource_fields)
    def get(self, asset_id):
        asset = Asset.query.filter_by(identifier=asset_id).first()
        if asset is None:
            return '', 404
        return asset, 200


class AssetCollectionResource(Resource):
    '''
    View for looking at lists of assets
    '''

    def __init__(self):
        self.get_reqparse = reqparse.RequestParser()
        # TODO force to int
        self.get_reqparse.add_argument('number')
        # TODO force one of the two types
        self.get_reqparse.add_argument('sort')

    @marshal_with(asset_resource_fields)
    def get(self):
        args = self.get_reqparse.parse_args()
        asset_query = Asset.query
        if args['sort'] is not None:
            sort_type = args['sort']
            if sort_type == 'reverse':
                asset_query = asset_query.order_by(desc(text("title")))
            else:
                print('sort normal')
                asset_query = asset_query.order_by(text("title"))
        if args['number'] is not None:
            number = args['number']
            assets = asset_query.limit(int(number)).all()
        else:
            assets = asset_query.all()
        return assets


class AssetCreditAssociationResource(Resource):

    def __init__(self):
        pass

    @marshal_with(credit_resource_fields)
    def get(self, asset_id):
        '''
        for asset_id list credits
        '''
        asset = Asset.query.filter_by(identifier=asset_id).first()
        if asset is None:
            return '', 404
        return asset.credits

    def post(self, asset_id, credit_id):
        error = insert_credit_asset_association(int(asset_id), int(credit_id))
        if error is not None:
            return error, 400
        return '', 201


class CreditAssetAssociationResource(Resource):
    def __init__(self):
        pass

    @marshal_with(asset_resource_fields)
    def get(self, credit_id):
        '''
        for asset_id list credits
        '''
        credit = Credit.query.filter_by(identifier=credit_id).first()
        if credit is None:
            return '', 404
        return credit.assets
