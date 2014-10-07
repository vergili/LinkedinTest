# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db



class Linkedin(db.Model):

    __tablename__ = 'linkedin'

    id               = Column(db.Integer, primary_key=True)
    name             = Column(db.Text(collation='utf8_general_ci')) 
    heading          = Column(db.Text(collation='utf8_general_ci')) 
    location         = Column(db.Text(collation='utf8_general_ci')) 
    summary          = Column(db.Text(collation='utf8_general_ci')) 
    education        = Column(db.Text(collation='utf8_general_ci')) 
    positions        = Column(db.Text(collation='utf8_general_ci')) 





