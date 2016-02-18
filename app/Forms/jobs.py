from wtforms import Form, TextField, validators, ValidationError, \
                    SelectMultipleField, SelectField
from wtforms.widgets import TextArea
from app import savvy_collection, jobs_collection
from flask import flash
from datetime import datetime
from bson.objectid import ObjectId
from app.Helpers.Constant import *

class jobForm(Form):
    title   = TextField('title', [validators.Required()])
    jobType = SelectField('jobType',
                           [validators.Required()],
                           coerce=int,
                           choices = [(0,'Casual'),
                                      (1,'Temp'),
                                      (2,'Contract'),
                                      (3,'Part-time'),
                                      (4,'Full-time'),
                                      (5,'Volunteer')])

    description = TextField('description', [validators.Required()], widget=TextArea())

    availability = SelectMultipleField('availability',
                                       [validators.Optional()],
                                       choices = [('0','Monday'),
                                                  ('1','Tuesday'),
                                                  ('2','Wednesday'),
                                                  ('3','Thursday'),
                                                  ('4','Friday'),
                                                  ('5','Saturday'),
                                                  ('6','Sunday')])


    def __init__(self, *args, **kwargs):
        self.email = args[1]
        Form.__init__(self, args[0], **kwargs)
        self.timeStamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    def validate(self,user):
        # insert into database
        job = {
            "title"         : self.title.data,
            "availability"  : self.availability.data,
            "jobType"       : self.jobType.data,
            "description"   : self.description.data.rstrip(),
            "timeStamp"     : self.timeStamp,
        }

        employerId = user['_id']
        jobs_collection.update({'employerId': employerId},
                               {"$set": {self.timeStamp: job}})
        savvy_collection.update({EMAIL: self.email},
                                {"$addToSet": {"jobs":self.timeStamp}})

        return True
