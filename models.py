'''
corresponds to what is usually refered to as model today in mvc
but should be considered totally seperate from the mvc
if using the traditional definition of mvc
basically holds our data storage logic and buisness logic
Buisness logic should edventually get split out
'''

import arrow
from sqlalchemy_utils.types.arrow import ArrowType
from sqlalchemy.orm import relationship

from database import db



#potentially casscading deletes
asset_credit_table = db.Table('AssetCredit',
                              db.Column('asset_id', db.Integer,
                                        db.ForeignKey('asset.identifier')),
                              db.Column('credit_id', db.Integer,
                                        db.ForeignKey('credit.identifier')))

def insert_credit_asset_association(asset_id, credit_id):
    asset = Asset.query.filter_by(identifier=asset_id).first()
    if asset is None:
        return 'need a valid asset_id'

    credit = Credit.query.filter_by(identifier=credit_id).first()
    if credit is None:
        return 'need a valid credit_id'

    asset.credits.append(credit)
    db.session.add(asset)
    db.session.commit()
    return None


class Asset(db.Model):
    # for something more complex also might want a uuid or something
    identifier = db.Column('identifier', db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    thumbnail_url = db.Column(db.String) #TODO validation bla
    creation_date = db.Column(ArrowType)
    credits = relationship("Credit",
                           secondary=asset_credit_table,
                           backref="assets")
    def __init__(self, title, description, thumbnail_url):
        self.title = title
        self.description = description
        self.thumbnail_url = thumbnail_url
        self.creation_date = arrow.utcnow()
        #for more complex apps this should get seperated out
        #some times you may want to create many objects before commit
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,title, description, thumbnail_url):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if thumbnail_url is not None:
            self.thumbnail_url = thumbnail_url
        db.session.add(self)
        db.session.commit()


class Credit(db.Model):
    '''
    Not quite sure how these should work so left pretty generic
    For example we could force them to associated with an Asset
    Also potentially there should be only one credit like director peter jackson
    that is enfoced as a singular and used everywhere
    But I just left it very flexible
    '''
    identifier = db.Column('identifier', db.Integer, primary_key=True)
    job_type = db.Column(db.String)
    name = db.Column(db.String)

    def __init__(self, job_type, name):
        self.job_type = job_type
        self.name = name
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,name, job_type):
        if name is not None:
            self.name = name
        if job_type is not None:
            self.job_type = job_type
        db.session.add(self)
        db.session.commit()


