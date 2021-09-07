from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponseRedirect
from .forms import CustomUserForm, UserProfileForm, ExtendUserForm, ChangeCustomerProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from laundryManagementSystem.addtocart.models import Order
from django.contrib.auth import logout 

# Create your views here.
def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #insert into DB
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'customer/signup.html', {'form':form})


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and userProfileForm.is_valid():
            user = form.save()
            profile = userProfileForm.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect('laundry/login/')

    else:
        form = CustomUserForm()
        userProfileForm = UserProfileForm()

    context = {'form':form, 'profile':UserProfileForm}
    return render(request, 'customer/index.html', context)


def customerlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('index2/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}
    return render(request, 'laundryman/login.html', context) 


# Demo for testing
def registerDemo(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        profile_form = ExtendUserForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile=profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.info(request, "You account has been created successful, login here!")
            return HttpResponseRedirect('customer/login/')

    else:
        form = CustomUserForm()
        profile_form = ExtendUserForm() 

    return render(request, 'customer/index2.html', {'form':form, 'profile_form':profile_form}) 


def customerProfile(request):
    # data that i need is customer username, email, phone number
    accessingUser = User.objects.get(username=request.user.username)
    userPro = UserProfile0.objects.get(user = request.user)
    print(str(accessingUser))
    email = accessingUser.email
    name = accessingUser.username
    phone = userPro.phone
    print(name, email, phone)
    context = {'email': email, 'name':name, 'phone': phone}
    return render(request, 'customer/customer_profile.html', context)

def changeProfile(request):
    if request.method == 'POST':
        form = ChangeCustomerProfile(request.POST)
        user = User.objects.get(username = request.user.username)
        print(user)
        profile = UserProfile0.objects.get(user = request.user)

        if user and profile:
            if form.is_valid():
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                print(user.email)
                user.save()
                profile.phone = form.cleaned_data['contact']
                profile.save
                messages.success(request, "Your information has successful updated")
                return HttpResponseRedirect('/customerProfile/')
            
    else:
        form = ChangeCustomerProfile()
        profile = UserProfile0()
    context = {'form':form}
    return render(request, 'customer/updateProfile.html', context)


class ViewOrders(TemplateView):
    template_name = "customer/customer_order.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allOrdersByThisUser = Order.objects.filter(ordered_by = self.request.user).order_by('-created_at')
        
        print(str(allOrdersByThisUser))
        context = {}
        if allOrdersByThisUser:
            context['order_qs'] = allOrdersByThisUser
        else:
            context = {}
        return context

def deleteOrder(request, order_id):
    # this is just a link if its placed then we track the clicked order_id and delete it 
    if order_id:
        orderToTrash = Order.objects.get(id=order_id)
        orderToTrash.delete()
        return HttpResponseRedirect('/customerOrders/')
    else:
        print("Oooh i want that order id")
    allOrdersByThisUser = Order.objects.filter(ordered_by = self.request.user).order_by('-created_at')
    context = {'order_qs': allOrdersByThisUser}

    return render(request, 'customer/customer_order.html', context)




def logout_request(request):
    # Before logged out first check if the session of cart_id exists 
    cart_id =  request.session.get("cart_id", None)
    if cart_id:
        # then here delete session
        del request.session['cart_id']
        print("cart session is exist and its already been deleted!")
    else:
        print("cart session is not exist, its None so there is no need to delete it!")
    logout(request)
    messages.info(request, "logged out successful")
    return HttpResponseRedirect('/')