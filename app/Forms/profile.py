from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField,\
                    validators, ValidationError, RadioField, \
                    DateTimeField, SelectMultipleField
from app import savvy_collection
from flask import flash

class profileFormEmployer(Form):
    businessName = TextField('businessName')
    contactName = TextField('contactName')
    phoneNumber = TextField('phoneNumber')
    website = TextField('website')
    streetAddress = TextField('streetAddress')
    hiring = RadioField('hiring', choices = [('0', 'Yes'), ('1', 'No')])

    def __init__(self, *args, **kwargs):
        self.username = args[0]
        Form.__init__(self, args[1], **kwargs)
        user = savvy_collection.find_one({"username": self.username})
        self.category = user['category'] #why?

    def validate(self):
        # insert into database
        user = {
            "businessName"      : self.businessName.data,
            "contactName"       : self.contactName.data,
            "phoneNumber"       : self.phoneNumber.data,
            "website"           : self.website.data.rstrip(),
            "streetAddress"     : self.streetAddress.data,
            "hiring"            : self.hiring.data
        }

        savvy_collection.update({"username": self.username},
                                {"$set": user})
        return True

class profileFormEmployee(Form):
    firstName       = TextField('firstName')
    lastName        = TextField('lastName')
    phoneNumber     = TextField('phoneNumber')
    introduction    = TextField('introduction')
    birthday        = DateTimeField('birthday', format='%d/%m/%y')
    skills          = TextField('skills')

    gender = RadioField('gender',
                        choices = [(0,'Male'), (1,'Female')])

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

    def __init__(self, *args, **kwargs):
        self.username = args[0]
        Form.__init__(self, args[1], **kwargs)
        self.user = savvy_collection.find_one({"username":self.username})
        self.category = self.user['category'] #why?

    def validate(self):
        savvy_collection.update(
            { "username": self.username },
            { "$set": {
                "firstName"     : self.firstName.data.rstrip(),
                "lastName"      : self.lastName.data.rstrip(),
                "phoneNumber"   : self.phoneNumber.data.rstrip(),
                "gender"        : self.gender.data,
                "birthday"      : self.birthday.data,
                "residency"     : self.residency.data,
                "introduction"  : self.introduction.data,
                "education"     : self.education.data,
                "availability"  : self.availability.data,
                "skills"        : self.skills.data }
            })

        return True
