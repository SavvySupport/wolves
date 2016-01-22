from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField,\
                    validators, ValidationError, RadioField, \
                    DateTimeField, SelectMultipleField, SelectField
from wtforms.widgets import TextArea
from app import savvy_collection
from flask import flash

class employerForm(Form):
    businessName    = TextField('businessName')
    contactName     = TextField('contactName')
    phoneNumber     = TextField('phoneNumber')
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

    def validate(self, user):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        return True

    def update(self):
        user = {
            "businessName"      : self.businessName.data,
            "contactName"       : self.contactName.data,
            "phoneNumber"       : self.phoneNumber.data,
            "website"           : self.website.data.rstrip(),
            "streetAddress"     : self.streetAddress.data
        }

        savvy_collection.update({"username": current_user.get_id()['username']},
                                {"$set": user})

class candidateForm(Form):
    firstName       = TextField('firstName')
    lastName        = TextField('lastName')
    phoneNumber     = TextField('phoneNumber')
    skills          = TextField('skills')
    birthday        = DateTimeField('birthday', format='%d/%m/%y')
    introduction    = TextField('introduction')
    location        = TextField('location')

    gender = SelectField('gender',
                         choices = [(0,'Male'),
                                    (1,'Female'),
                                    (2,'Other')],
                         default = 0)

    residency = RadioField('residency',
                           [validators.Optional()],
                           choices = [(0,'Citizen'),
                                      (1,'Permanent Resident'),
                                      (2,'Temporary Resident Visa'),
                                      (3,'Student Visa'),
                                      (4,'Other')])

    education = RadioField('education',
                           [validators.Optional()],
                           choices = [(0,'Finishing High School'),
                                      (1,'Completed High School'),
                                      (2,'Finishing Tafe/Apprenticeship'),
                                      (3,'Completed Tafe/Apprenticeship'),
                                      (4,'Finishing University'),
                                      (5,'Completed University')])

    availability = SelectMultipleField('availability',
                                       [validators.Optional()],
                                       choices = [('0','Monday'),
                                                  ('1','Tuesday'),
                                                  ('2','Wednesday'),
                                                  ('3','Thursday'),
                                                  ('4','Friday'),
                                                  ('5','Saturday'),
                                                  ('6','Sunday')])

    jobStatus = RadioField('jobStatus',
                           [validators.Optional()],
                           choices = [('0','Yes'), ('1','No')])

    def __init__(self, *args, **kwargs):
        self.type = 'candidate'
        Form.__init__(self, args[1], **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        user = {
            "firstName"     : self.firstName.data.rstrip(),
            "lastName"      : self.lastName.data.rstrip(),
            "phoneNumber"   : self.phoneNumber.data.rstrip(),
            "gender"        : self.gender.data,
            "birthday"      : self.birthday.data,
            "residency"     : self.residency.data,
            "introduction"  : self.introduction.data,
            "education"     : self.education.data,
            "availability"  : self.availability.data,
            "skills"        : self.skills.data,
            "location"      : self.location.data
        }

        savvy_collection.update(
            { "username": current_user.get_id()['username'] },
            { "$set": user })

        return True

    def prepopulate(self, user):
        self.firstName.data     = user.get('firstName', '')
        self.lastName.data      = user.get('lastName', '')
        self.phoneNumber.data   = user.get('phoneNumber', '')
        self.gender.data        = user.get('gender', '')
        self.birthday.data      = user.get('birthday', '')
        self.residency.data     = user.get('residency', '')
        self.introduction.data  = user.get('introduction', '')
        self.education.data     = user.get('education', '')
        self.availability.data  = user.get('availability', '')
        self.skills.data        = user.get('skills', '')
        self.jobStatus.data     = user.get('jobStatus', '')
        self.location.data      = user.get('location', '')
