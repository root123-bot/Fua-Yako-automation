from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LaundryProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tele = models.CharField(max_length=10)   
    photo = models.ImageField(upload_to='images/')
    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    ward = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    location = models.TextField(max_length=200)
    account_number = models.CharField(max_length=10)
    category = models.CharField(max_length=30, default="Laundryman")  
    def __str__(self):  
        return self.user.username



"""
class FnameBackend(object):  
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(first_name=username)
        except User.MultipleObjectsReturned:
            user = User.objects.filter(first_name=username).order_by('id').first()
        except User.DoesNotExist:  
            return None  
        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class FnameBackend():
    def authenticate(self, request, username, password):
        try:
            user = User.objects.get(first_name = username)
            this = user
            print(user.username)
            # Check if the associated user has an brela number/ if its for the laundryman try to check if the entered user exist in CompanyProfile/ laundryman
            # create the qs  containing all the companyprofiles
            companies = LaundryProfile.objects.all()
            print(str(companies))
            success = user.check_password(password)
            # This condition will not be found in companies in that case we should query the companyProfile with this user
            #associateduser = companyProfile.objects.get(user = user) 
            if LaundryProfile.objects.filter(user = this):
                print(str(LaundryProfile.objects.filter(user=this)))
                dah = LaundryProfile.objects.filter(user=this)
                elementOfOne = dah[0]
                print("everything works fine!")
                print(str(elementOfOne))
                if elementOfOne in companies:
                    print("Yes its passed")
                    if success:
                        return user
            else:
                print("The  profile is not found")
        except User.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None

"""

class FnameBackend():
    def authenticate(self, request, username, password):
        try:
            # How to do query to get the user object which has the phone
            # lau = LaundryProfile.user_set.all()
            user = User.objects.get(email = username)
            this = user
            print(user.username)
            # Check if the associated user has an brela number/ if its for the laundryman try to check if the entered user exist in CompanyProfile/ laundryman
            # create the qs  containing all the companyprofiles
            companies = LaundryProfile.objects.all()
            print(str(companies))
            success = user.check_password(password)
            # This condition will not be found in companies in that case we should query the companyProfile with this user
            #associateduser = companyProfile.objects.get(user = user) 
            if LaundryProfile.objects.filter(user = this):
                print(str(LaundryProfile.objects.filter(user=this)))
                dah = LaundryProfile.objects.filter(user=this)
                elementOfOne = dah[0]
                print("everything works fine, but I'm inside the laundryBackend!")
                print(str(elementOfOne))
                if elementOfOne in companies:
                    print("Yes its passed")
                    if success:
                        return user
            else:
                print("The  profile is not found")
        except User.DoesNotExist:
            pass
        return None
    
    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None
