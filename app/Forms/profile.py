from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError, RadioField,DateTimeField,SelectMultipleField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.Models.User import User
from app import savvy_collection
from flask.ext.login import login_user
from flask import flash
from hashlib import md5
import os, subprocess


class profileFormEmployer(Form):
    #form for employers

    businessName = TextField('businessName')
    contactName = TextField('contactName')
    phoneNumber = TextField('phoneNumber')
    website = TextField('website')
    streetAddress = TextField('streetAddress')
    hiring = RadioField('hiring', choices=[('0','Yes'),('1','No')])

    def __init__(self, *args, **kwargs):
        self.username = args[0]
        Form.__init__(self, args[1], **kwargs)
        user = savvy_collection.find_one({"username":self.username})
        self.category = user['category']
        self.ownProfile = "yes" #will check this condition in html, to decide if user viewing own profile or not.



    def validate(self):

        # insert into database
        user = {"businessName": self.businessName.data,
        "contactName": self.contactName.data,
        "phoneNumber"   : self.phoneNumber.data,
        "website"  : self.website.data.rstrip(),
        "streetAddress"   : self.streetAddress.data,
        "hiring"    : self.hiring.data
        }

        savvy_collection.update({"username":self.username},{"$set":user})

        return True

    def prepopulate(self):
        user = savvy_collection.find_one({"username":self.username})
        self.businessName.data = user['businessName']
        self.contactName.data = user['contactName']
        self.phoneNumber.data = user['phoneNumber']
        self.website.data = user['website']
        self.streetAddress.data = user['streetAddress']
        self.hiring.data = user['hiring']


class profileFormEmployee(Form):
    #form for employees

    #profilePicture = FileField('profilePicture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    firstName = TextField('firstName')
    lastName = TextField('lastName')
    phoneNumber = TextField('phoneNumber')
    birthday  = DateTimeField('birthday', format='%d/%m/%y')
    gender = RadioField('gender', choices=[(0,'Male'), (1,'Female')])
    residency = RadioField('residency', [validators.Optional()], choices=[(0,'Citizen'),(1,'Permanent Resident'),(2,'Temporary Resident Visa'),(3,'Student Visa'),(4,'Other')])
    introduction = TextField('introduction')
    education = RadioField('education', [validators.Optional()],choices=[(0,'Finishing High School'),(1,'Completed High School'),(2,'Finishing Tafe/Apprenticeship'),(3,'Completed Tafe/Apprenticeship'),(4,'Finishing University'),(5,'Completed University')])
    availability = SelectMultipleField('availability', [validators.Optional()], choices=[('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')])
    skills = TextField('skills')
    jobStatus = RadioField('jobStatus', [validators.Optional()], choices=[('0','Yes'),('1','No')])

    def __init__(self, *args, **kwargs):
        self.username = args[0]
        Form.__init__(self, args[1], **kwargs)
        self.user = savvy_collection.find_one({"username":self.username})
        self.category = self.user['category']
        self.ownProfile = "yes" #as condition in profile.html

    #add places available to work in


    def validate(self):

        savvy_collection.update({"username":self.username},{"$set":{
        "firstName": self.firstName.data.rstrip(),
        "lastName": self.lastName.data.rstrip(),
        "phoneNumber"   : self.phoneNumber.data.rstrip(),
        "gender"  : self.gender.data,
        "birthday"   : self.birthday.data,
        "residency"    : self.residency.data,
        "introduction"  : self.introduction.data,
        "education" : self.education.data,
        "availability"  : self.availability.data,
        "skills"    : self.skills.data}})

        return True

    def prepopulate(self):
        user = savvy_collection.find_one({"username":self.username})
        self.firstName.data = user['firstName']
        self.lastName.data = user['lastName']
        self.phoneNumber.data = user['phoneNumber']
        self.gender.data = user['gender']
        self.birthday.data = user['birthday']
        self.residency.data = user['residency']
        self.introduction.data = user['introduction']
        self.education.data = user['education']
        self.availability.data = user['availability']#
        self.skills.data = user['skills']
        self.jobStatus.data = user['jobStatus']
