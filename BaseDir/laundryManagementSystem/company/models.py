from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here

class Task(models.Model):
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SignUp(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=30)
    password = models.CharField(max_length =40)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput()
        }


class companyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length = 20)
    mobile = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=30, default="Company")
    account_number = models.CharField(max_length=10)


    def __str__(self):
        return self.user.username




"""
class CompanyBackend(object):  
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # How to link the User and CompanyProfile db  >>>>> User.Company, hapa ni lazima kwanza tupate field ya brela number
            # brela number >>> regNo = companyProfile.objects.get(reg_no = brela_no)
            # why don't capture the email and check if it has the associated brela number
            user=User.objects.get(email=username)
            companies = companyProfile.objects.all()
            print(str(companies))
            success = user.check_password(password)
            if user in companies and success:
                print("Yes")
                return user
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
"""

class CompanyBackend():   #Here you should use brela_number associated with email written >>>> brela_number exists
    def authenticate(self, request, username, password):
        try:   
            user = User.objects.get(email = username)   # We use email here
            this = user
            print(user.username)
            # Check if the associated user has an brela number/ if its for the laundryman try to check if the entered user exist in CompanyProfile/ laundryman
            # create the qs  containing all the companyprofiles
            companies = companyProfile.objects.all()
            print(str(companies))
            success = user.check_password(password)
            # This condition will not be found in companies in that case we should query the companyProfile with this user
            #associateduser = companyProfile.objects.get(user = user) 
            if companyProfile.objects.filter(user = this):
                print(str(companyProfile.objects.filter(user=this)))
                dah = companyProfile.objects.filter(user=this)
                elementOfOne = dah[0]
                print("everything works fine!, I use company backend")
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
