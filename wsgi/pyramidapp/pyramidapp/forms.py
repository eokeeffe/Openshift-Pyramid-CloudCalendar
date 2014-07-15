from wtforms import (Form, 
    BooleanField, TextField, 
    TextAreaField, validators, 
    PasswordField, DateField, DateTimeField)
from wtforms import HiddenField
from wtforms.validators import required,Email,EqualTo,Length

strip_filter = lambda x: x.strip() if x else None

class CreateUser(Form):
    name = TextField('User name', [validators.Length(min=1, max=80),required()],
        filters=[strip_filter])
    password = PasswordField('password', [validators.Length(min=6,max=80),validators.equal_to('confirm_pass')],
        filters=[strip_filter])
    confirm_pass = PasswordField('confirm password')

class AllowUser(Form):
    title = TextField('User to share with', [Length(min=1, max=80),required()],
        filters=[strip_filter])

class FindEvent(Form):
    title = TextField('Event Name', [Length(min=1, max=80),required()],
        filters=[strip_filter])

class RevokeUser(Form):
    name = TextField('User to revoke sharing for', [Length(min=1, max=80),required()],
        filters=[strip_filter])

class CreateEvent(Form):
    title = TextField('Event Name', [Length(min=1, max=80),required()],
        filters=[strip_filter])
    description = TextAreaField('Event Desciption', [Length(min=0, max=80)],
        filters=[strip_filter])
    start = DateTimeField('Starting Event Date', format='%d-%m-%Y %H:%M:%S',validators=[required()])
    end = DateTimeField('Ending Event Date', format='%d-%m-%Y %H:%M:%S')
    allDay = BooleanField('Occurring All Day')
    url = TextField('URL of the event')

class EditEvent(CreateEvent):
    id = HiddenField()

class RemoveEvent(Form):
    title = TextField('Event Name', [Length(min=1, max=80),required()],
        filters=[strip_filter])
    description = TextAreaField('Event Desciption', [Length(min=0, max=80)],
        filters=[strip_filter])
    start = DateTimeField('Starting Event Date', format='%d-%m-%Y %H:%M:%S',validators=[required()])
    end = DateTimeField('Ending Event Date', format='%d-%m-%Y %H:%M:%S')
    allDay = BooleanField('Occurring All Day')
    url = TextField('URL of the event')

class BlogCreateForm(Form):
    title = TextField('Entry title', [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    body = TextAreaField('Entry body', [validators.Length(min=1)],
                         filters=[strip_filter])

class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()