from app.Models.User import User
from app import savvy_collection
from flask import flash

class viewProfile(): 
    def __init__(self, *args, **kwargs):
        self.username = args[0]
        print (self.username)
        user = savvy_collection.find_one({"username":self.username})
        self.category = user['category']
        self.ownProfile = "no"
        self.businessName = user['businessName']
        self.contactName = user['contactName']
        self.phoneNumber = user['phoneNumber']
        self.website = user['website']
        self.streetAddress = user['streetAddress']
        self.hiring = user['hiring']
        self.lastName = user['lastName']
        self.firstName = user['firstName']
        self.phoneNumber = user['phoneNumber']
        self.gender = user['gender']
        self.birthday = user['birthday']
        self.residency = user['residency']
        self.introduction = user['introduction']
        self.education = user['education']
        self.availability = user['availability']
        self.skills = user['skills']
