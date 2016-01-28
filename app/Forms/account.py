from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField,\
                    validators, ValidationError, RadioField, \
                    DateTimeField, SelectMultipleField, SelectField
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

    # availability = SelectMultipleField('availability',
    #                                    choices = [(MON,'Monday'),
    #                                               (TUE, 'Tuesday'),
    #                                               (WED, 'Wednesday'),
    #                                               (THU, 'Thursday'),
    #                                               (FRI, 'Friday'),
    #                                               (SAT, 'Saturday'),
    #                                               (SUN, 'Sunday')])

    availability = SelectField('availability',
                                coerce=int,
                                choices = [(1, '1 day per week'),
                                           (2, '2 days per week'),
                                           (3, '3 days per week'),
                                           (4, '4 days per week'),
                                           (5, '5 days per week'),
                                           (6, '6 days per week'),
                                           (7, '7 days per week')],
                                default = 1)

    # jobStatus = RadioField('jobStatus',
    #                         choices = [(YES, 'Yes'), (NO, 'No')])

    def __init__(self, *args, **kwargs):
        self.type = 'candidate'
        Form.__init__(self, args[1], **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    print(self.birthday.data)
                    print(fieldName, err)
            return False
        return True

    def update(self, username):
        user = {
            "firstName"     : self.firstName.data.rstrip(),
            "lastName"      : self.lastName.data.rstrip(),
            "phoneNumber"   : self.phoneNumber.data.rstrip(),
            "gender"        : self.gender.data,
            "birthday"      : str(self.birthday.data),
            "residency"     : self.residency.data,
            "about"         : self.about.data,
            "education"     : self.education.data,
            "availability"  : self.availability.data,
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
        self.birthday.data      = datetime.strptime(str(user.get('birthday', '')),'%Y-%m-%d')
        self.residency.data     = user.get('residency', '')
        self.about.data         = user.get('about', '')
        self.education.data     = user.get('education', '')
        self.availability.data  = user.get('availability', '')
        self.skills.data        = ','.join(user.get('skills', None))
        self.location.data      = user.get('location', '')
