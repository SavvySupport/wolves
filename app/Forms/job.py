from wtforms import Form, BooleanField, TextField, TextAreaField, \
                    validators, ValidationError, SelectMultipleField
from wtforms.widgets import TextArea
from app import savvy_collection, jobs_collection
from flask import flash
from datetime import datetime
from app.Helpers.Constant import *

class jobForm(Form):
    title        = TextField(TITLE, [validators.Required()])
    description  = TextField(DESCR, [validators.Required()], widget=TextArea())
    availability = SelectMultipleField(AVAILABILITY,
                                       [validators.Optional()],
                                       choices = [MON, TUE, WED, THU, FRI, SAT, SUN, HOL])

    residency = SelectMultipleField(RESIDENCY,
                                    [validators.Optional()],
                                    choices = [CITIZEN, PR, TR, STUDENT, OTHER])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, args[0], **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            message = ''
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    message = message + fieldName + ': ' + err + '\n'
            flash(message, 'error')
            return False
        return True

    def update(self, user):
        job = {
            TITLE         : self.title.data,
            AVAILABILITY  : self.availability.data,
            DESCR         : self.description.data.rstrip(),
        }

        timeStamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        id = user['_id']
        jobs_collection.update({EMPLOYERID: id},
                               {"$set": {timeStamp: job}})

        savvy_collection.update({EMAIL: user[EMAIL]},
                                {"$addToSet": {"jobs": timeStamp}})
