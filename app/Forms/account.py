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
    businessName    = TextField(BUSINESS)
    contactName     = TextField(CONTACT)
    phoneNumber     = TextField(PHONE, [validators.length(min=10),
                                        validators.Optional(),
                                        validators.regexp('^[0-9]+$')])
    website         = TextField(WEBSITE)
    streetAddress   = TextField(ADDRESS)
    about           = TextField(ABOUT, widget=TextArea())

    def __init__(self, *args, **kwargs):
        self.type = EMPL
        self.user = args[0]
        Form.__init__(self, args[1], **kwargs)


    def prepopulate(self, user):
        self.businessName.data  = user.get(BUSINESS, '')
        self.contactName.data   = user.get(CONTACT, '')
        self.phoneNumber.data   = user.get(PHONE, '')
        self.website.data       = user.get(WEBSITE, '')
        self.streetAddress.data = user.get(ADDRESS, '')

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
            BUSINESS    : self.businessName.data,
            CONTACT     : self.contactName.data,
            PHONE       : self.phoneNumber.data,
            WEBSITE     : self.website.data.rstrip(),
            ADDRESS     : self.streetAddress.data
        }

        savvy_collection.update({USERNAME: username},
                                {"$set": user})

class candidateForm(Form):
    firstName       = TextField(FNAME)
    lastName        = TextField(LNAME)
    phoneNumber     = TextField(PHONE, [validators.length(min=10),
                                        validators.Optional(),
                                        validators.regexp('^[0-9]+$')])
    skills          = TextField(SKILLS)
    birthday        = DateField(BIRTHDAY)
    about           = TextField(ABOUT, widget=TextArea())
    location        = TextField(LOCATION)

    gender = SelectField(GENDER,
                         choices = [MALE, FEMALE, OTHER],
                         default = MALE[CODE])

    residency = SelectField(RESIDENCY,
                            choices = [CITIZEN,
                                       PR,
                                       TR,
                                       STUDENT,
                                       OTHER],
                            default = CITIZEN[CODE])

    education = SelectField(EDUCATION,
                            choices = [HS,
                                       HS_COMPLETED,
                                       TAFE,
                                       TAFE_COMPLETED,
                                       UNI,
                                       UNI_COMPLETED,
                                       NA],
                            default = UNI[CODE])

    availability_choices = [NA, MORNING, AFTERNOON, ALL_DAY]
    monday      = SelectField(MON[TEXT], choices=availability_choices, default='Unavailable')
    tuesday     = SelectField(TUE[TEXT], choices=availability_choices, default='Unavailable')
    wednesday   = SelectField(WED[TEXT], choices=availability_choices, default='Unavailable')
    thursday    = SelectField(THU[TEXT], choices=availability_choices, default='Unavailable')
    friday      = SelectField(FRI[TEXT], choices=availability_choices, default='Unavailable')
    saturday    = SelectField(SAT[TEXT], choices=availability_choices, default='Unavailable')
    sunday      = SelectField(SUN[TEXT], choices=availability_choices, default='Unavailable')
    holiday     = SelectField(HOL[TEXT], choices=availability_choices, default='Unavailable')

    def __init__(self, *args, **kwargs):
        self.type = CAND
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
            MON[TEXT]       : self.monday.data,
            TUE[TEXT]       : self.tuesday.data,
            WED[TEXT]       : self.wednesday.data,
            THU[TEXT]       : self.thursday.data,
            FRI[TEXT]       : self.friday.data,
            SAT[TEXT]       : self.saturday.data,
            SUN[TEXT]       : self.sunday.data,
            HOL[TEXT]       : self.holiday.data,
        }

        tmp = (self.skills.data.rstrip()).split(',')
        skills = []
        for skill in tmp:
            if skill != '':
                skills.append(skill)

        user = {
            FNAME         : self.firstName.data.rstrip(),
            LNAME         : self.lastName.data.rstrip(),
            PHONE         : self.phoneNumber.data.rstrip(),
            GENDER        : self.gender.data,
            BIRTHDAY      : str(self.birthday.data),
            RESIDENCY     : self.residency.data,
            ABOUT         : self.about.data,
            EDUCATION     : self.education.data,
            AVAILABILITY  : availability,
            SKILLS        : skills,
            LOCATION      : self.location.data
        }

        savvy_collection.update(
            { USERNAME: username },
            { "$set": user })

        return True

    def prepopulate(self, user):
        self.firstName.data     = user.get(FNAME, '')
        self.lastName.data      = user.get(LNAME, '')
        self.phoneNumber.data   = user.get(PHONE, '')
        self.gender.data        = user.get(GENDER, '')
        self.residency.data     = user.get(RESIDENCY, '')
        self.about.data         = user.get(ABOUT, '')
        self.education.data     = user.get(EDUCATION, '')
        self.skills.data        = ','.join(user.get(SKILLS, None))
        self.location.data      = user.get(LOCATION, '')
        if user.get(BIRTHDAY, None):
            self.birthday.data  = datetime.strptime(str(user.get(BIRTHDAY, None)), '%Y-%m-%d')

        availability = user.get(AVAILABILITY, None)

        if availability:
            try:
                self.monday.data    = availability.get(MON[TEXT], NA[CODE])
                self.tuesday.data   = availability.get(TUE[TEXT], NA[CODE])
                self.wednesday.data = availability.get(WED[TEXT], NA[CODE])
                self.thursday.data  = availability.get(THU[TEXT], NA[CODE])
                self.friday.data    = availability.get(FRI[TEXT], NA[CODE])
                self.saturday.data  = availability.get(SAT[TEXT], NA[CODE])
                self.sunday.data    = availability.get(SUN[TEXT], NA[CODE])
                self.holiday.data   = availability.get(HOL[TEXT], NA[CODE])
            except:
                pass
