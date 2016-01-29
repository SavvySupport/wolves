from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField,\
                    validators, ValidationError, RadioField, \
                    DateTimeField, SelectMultipleField, SelectField, widgets
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
from app import savvy_collection
from flask import flash
from app.Helpers.Constant import *
from datetime import datetime, date

class employerForm(Form):
    businessName    = TextField('businessName')
    contactName     = TextField('contactName')
    phoneNumber     = TextField('phoneNumber', [validators.length(min=10),
                                                validators.Optional(),
                                                validators.regexp('^[0-9]+$')])
    website         = TextField('website')
    streetAddress   = TextField('streetAddress')
    about           = TextField('about', widget=TextArea())

    def __init__(self, *args, **kwargs):
        self.type = 'employer'
        Form.__init__(self, args[1], **kwargs)

    def prepopulate(self, user):
        self.businessName.data  = user.get('businessName', '')
        self.contactName.data   = user.get('contactName', '')
        self.phoneNumber.data   = user.get('phoneNumber', '')
        self.website.data       = user.get('website', '')
        self.streetAddress.data = user.get('streetAddress', '')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    print(err)
            return False
        return True

    def update(self, username):
        user = {
            "businessName"      : self.businessName.data,
            "contactName"       : self.contactName.data,
            "phoneNumber"       : self.phoneNumber.data,
            "website"           : self.website.data.rstrip(),
            "streetAddress"     : self.streetAddress.data
        }

        savvy_collection.update({"username": username},
                                {"$set": user})

class candidateForm(Form):
    firstName       = TextField('firstName')
    lastName        = TextField('lastName')
    phoneNumber     = TextField('phoneNumber', [validators.length(min=10),
                                                validators.Optional(),
                                                validators.regexp('^[0-9]+$')])
    skills          = TextField('skills')
    birthday        = DateField('birthday')
    about           = TextField('about', widget=TextArea())
    location        = TextField('location')

    gender = SelectField('gender',
                         coerce=int,
                         choices = [(MALE, 'Male'),
                                    (FEMALE, 'Female'),
                                    (OTHER, 'Other')],
                         default = MALE)

    residency = SelectField('residency',
                            coerce=int,
                            choices = [(CITIZEN,'Citizen'),
                                       (PR,'Permanent Resident'),
                                       (TR,'Temporary Resident Visa'),
                                       (STUDENT,'Student Visa'),
                                       (OTHER,'Other')],
                            default = CITIZEN)

    education = SelectField('education',
                            coerce=int,
                            choices = [(HS, 'Finishing High School'),
                                       (HS_COMPLETED, 'Completed High School'),
                                       (TAFE, 'Finishing Tafe/Apprenticeship'),
                                       (TAFE_COMPLETED, 'Completed Tafe/Apprenticeship'),
                                       (UNI, 'Finishing University'),
                                       (UNI_COMPLETED, 'Completed University'),
                                       (NA, 'Not available')],
                            default = UNI)

    availability_choices = [('Unavailable', 'Unavailable'),
                            ('Morning', 'Morning'),
                            ('Afternoon', 'Afternoon'),
                            ('All day', 'All day')]
    monday      = SelectField('monday', choices=availability_choices, default='Unavailable')
    tuesday     = SelectField('tuesday', choices=availability_choices, default='Unavailable')
    wednesday   = SelectField('wednesday', choices=availability_choices, default='Unavailable')
    thursday    = SelectField('thursday', choices=availability_choices, default='Unavailable')
    friday      = SelectField('friday', choices=availability_choices, default='Unavailable')
    saturday    = SelectField('saturday', choices=availability_choices, default='Unavailable')
    sunday      = SelectField('sunday', choices=availability_choices, default='Unavailable')
    holiday     = SelectField('holiday', choices=availability_choices, default='Unavailable')

    def __init__(self, *args, **kwargs):
        self.type = 'candidate'
        Form.__init__(self, args[1], **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    print(fieldName, err)
                    print(self.availability.data)
            return False
        return True

    def update(self, username):
        availability = {
            "monday"        : self.monday.data,
            "tuesday"       : self.tuesday.data,
            "wednesday"     : self.wednesday.data,
            "thursday"      : self.thursday.data,
            "friday"        : self.friday.data,
            "saturday"      : self.saturday.data,
            "sunday"        : self.sunday.data,
            "holiday"       : self.holiday.data,
        }

        user = {
            "firstName"     : self.firstName.data.rstrip(),
            "lastName"      : self.lastName.data.rstrip(),
            "phoneNumber"   : self.phoneNumber.data.rstrip(),
            "gender"        : self.gender.data,
            "birthday"      : str(self.birthday.data),
            "residency"     : self.residency.data,
            "about"         : self.about.data,
            "education"     : self.education.data,
            "availability"  : availability,
            "skills"        : (self.skills.data.rstrip()).split(','),
            "location"      : self.location.data
        }

        savvy_collection.update(
            { "username": username },
            { "$set": user })

        return True

    def prepopulate(self, user):
        self.firstName.data     = user.get('firstName', '')
        self.lastName.data      = user.get('lastName', '')
        self.phoneNumber.data   = user.get('phoneNumber', '')
        self.gender.data        = user.get('gender', '')
        self.residency.data     = user.get('residency', '')
        self.about.data         = user.get('about', '')
        self.education.data     = user.get('education', '')
        self.skills.data        = ','.join(user.get('skills', None))
        self.location.data      = user.get('location', '')
        self.monday.data = 'Unavailable'
        if user.get('birthday', None):
            self.birthday.data  = datetime.strptime(str(user.get('birthday', None)), '%Y-%m-%d')

        availability = user.get('availability', None)

        if availability:
            try:
                self.monday.data    = availability.get('monday', '')
                self.tuesday.data   = availability.get('tuesday', '')
                self.wednesday.data = availability.get('wednesday', '')
                self.thursday.data  = availability.get('thursday', '')
                self.friday.data    = availability.get('friday', '')
                self.saturday.data  = availability.get('saturday', '')
                self.sunday.data    = availability.get('sunday', '')
                self.holiday.data   = availability.get('holiday', '')
            except:
                pass
