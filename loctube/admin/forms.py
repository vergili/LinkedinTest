# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import HiddenField, SubmitField, RadioField, DateField, TextField, TextAreaField
from wtforms.validators import (Required, Length, EqualTo, Email, NumberRange,  URL, AnyOf, Optional)



class LinkedinForm(Form):
    company      = TextField(u'Company', [Length(max=220)])
    submit = SubmitField(u'Save')