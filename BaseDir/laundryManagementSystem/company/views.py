from django.shortcuts import render, get_object_or_404
from .models import companyProfile
from django.db.models import Q 
from ..laundryman.models import LaundryProfile
from django.shortcuts import redirect
from .forms import CompanyForm, CProfile
from django.http import HttpResponseRedirect
#from .forms import LaundryForm, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..laundryman.models import LaundryProfile
from django.views.generic import TemplateView
from .forms import ChangeProfile, ChangePassword
from laundryManagementSystem.addtocart.models import Post, Product, Cart, Order
from django import forms
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.paginator import Paginator 
from laundryManagementSystem.Payment.models import Payment
from laundryManagementSystem.Payment.forms import PaymentForm
from django.core.mail import send_mail


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():


            form.save()
            print('Form is saved ')
            return HttpResponseRedirect('company/profile/')

    else:
        form = CompanyForm()
    context = {'form':form}  
    return render(request, 'company/index.html', context)

#@login_required(login_url='laundry/login/')
def profile(request):
        if request.method == 'POST':
            profile_form = CProfile(request.POST, request.FILES)
            account_numberForm = PaymentForm(request.POST)
            if profile_form.is_valid() and account_numberForm.is_valid():

                user = User.objects.latest('date_joined')
                # hapa kwenye user kumchukua user latest inaweza system ikachanganya ikamchukua user mwingine 
                # but for now iache hivihivi, kwa baadae tutatrack last entered username on creation of account and then 
                # relate with this user if they are the same or different, au naweza nikatumia 
                # session nikatrack username alioandika user on creation of account and then get the user object 
                # with that username, after getting that object I will save it on the profile user field


                # this latest method is used to deal online with the date
                # attributes not interger like id and its only  return
                # single value, so it's never iterable, so when you query
                # id it will throw an error  like
                # User.objects.latest('id=2') since its only deals with
                # the dates objects. THANKS StackOverFlow
                profile = profile_form.save(commit=False)

                profile.user = user
                profile.account_number = account_numberForm.cleaned_data['account_number']
                # profile.account_number = account_numberForm.cleaned_data['account_number']
                profile.save()
                PaymentObj = Payment.objects.create(username=profile.user.username, password = 'paschal123', account_number = account_numberForm.cleaned_data['account_number'], balance = 0)
                # get the profile of the latest individual to be registered
                #givenProfile = companyProfile.objects.get(user = user)
                #givenProfile.account_number = account_number.cleaned_data
                print('Profile form is saved')
                return HttpResponseRedirect('company/login/')
        else:
            profile_form = CProfile()
            account_numberForm = PaymentForm()
        context = {'profile_form': profile_form, 'accForm':account_numberForm}
        return render(request, 'company/profile.html', context)



def companylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('viewcompanyprofile/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}
    return render(request, 'company/realLogin.html', context)

# this will post a user profiles to our home for user to view
@login_required(login_url= 'laundry/login/')
def companiesView(request):  
    company_profiles = companyProfile.objects.all().only('id', 'user', 'reg_no', 'photo', 'address', 'category')
    #paginator = Paginator(company_profiles, 20)
    #page_number = request.GET.get('page')
    #company_profiles = paginator.get_page(page_number)
    if company_profiles:
        print("Yes there are companies")
        company_profiles = company_profiles
    else:
        company_profiles = None
    context = {'company_profiles': company_profiles}
    print(company_profiles)
    return render(request, 'companiesView.html', context)  
   

@login_required(login_url= 'laundry/login/')
def laundriesView(request):
    laundry_profiles = LaundryProfile.objects.all().only('id', 'user', 'photo', 'region', 'district', 'ward', 'street', 'location', 'category')
    if laundry_profiles:
        print("Yes there some laundries")
        laundry_profiles = laundry_profiles
        #paginator = Paginator(laundry_profiles, 20)
        #page_number = request.GET.get('page')
        #print(page_number) # it will GET this page parameter in our url
        #laundry_profiles = paginator.get_page(page_number)
    else: 
        laundry_profiles = None
    
    #context = {'product_list':product_list}
    context = {'laundry_profiles': laundry_profiles}
    print(laundry_profiles)
    return render(request, 'laundriesView.html', context)

def search(request):
    search_query = request.GET.get('search', '')
    if search_query:
        print(search_query)
        # the use of __icontains does not work with interger, its only works with 'string',
        # by default the companyProfile and LaundryProfile models have field of 'user' which 
        # references the user model, the user field of these models has reference username  
        # throught the User primary key which here for me is default one which is 'id' id is 
        # integer, so icontains can't do that in 'id', so we shall concatenate our 'user'
        # with 'username' with  this means that in that reference we need our 'user' field which is
        # by default reference all User model fields like id, username, email, password and so on.
        # So here to __icontains the username field which is string unlike id which is interger 
        # we use (user__username__icontains) this username is refered from the User model 'Usename'
        company = companyProfile.objects.filter(Q(user__username__icontains=search_query) | Q(address__icontains=search_query))
        laundry = LaundryProfile.objects.filter(Q(user__username__icontains=search_query) | Q(region__icontains=search_query) | Q(district__icontains=search_query) | Q(ward__icontains=search_query) | Q(street__icontains=search_query) | Q(location__icontains=search_query))
        print(laundry)
        print(company)
    else:
        company = companyProfile.objects.all()
        laundry = LaundryProfile.objects.all()
    context = {'company':company, 'laundry':laundry}  
    return render(request, 'results.html', context)



class CompanyProfileView(TemplateView):
    template_name = 'company/company_profile.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = companyProfile.objects.get(user=self.request.user)
        brela_no = profile.reg_no
        comp_name = profile.user.username
        email = profile.user.email
        mobile = profile.mobile
        pic = profile.photo.url
        anuani = profile.address

        context['brela'] = brela_no
        context['name'] = comp_name
        context['mobile'] = mobile
        context['pic'] = pic
        context['anuani'] = anuani
        context['pepe'] = email

        return context 
    
class EditProfile(TemplateView):
    template_name = 'company/editProfile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = companyProfile.objects.get(user=self.request.user)


def changeProfileForm(request):  
    if request.method == 'POST':
        form = ChangeProfile(request.POST, request.FILES)
        user = User.objects.get(username = request.user.username)
        print(user)
        profile = companyProfile.objects.get(user=request.user)
        pic = profile.photo.url
        if user and profile:
            if form.is_valid():
                user.email = form.cleaned_data['email']
                print(user.email)
                user.save()
                profile.photo = form.cleaned_data['profile_picture']
                profile.mobile = form.cleaned_data['contact']
                profile.address = form.cleaned_data['location']
                profile.save()
                messages.success(request, "Your information has successful updated")
                return HttpResponseRedirect('viewcompanyprofile/')
    else: 
        form = ChangeProfile()
        profile = companyProfile.objects.get(user=request.user)
        pic = profile.photo.url
    context = {'form':form, 'pic':pic}
    return render(request, 'company/editProfile.html', context)


def viewNotification(request):
    # When a user click link I want to drag all post information from the database and pass as contex variable to notification link
    # Fist all post records associated with this company
    username = request.user.username
    print(username)
    posts_qs = Post.objects.filter(receiver=username).order_by('-created_at')

    # Here on the view notification import the clicked
    # then get the queryset of all clicked post like
    # clicked = Post.objects.get(clicked=True)
    # after getting the qs on the template do
    # inside for q in qs:
    #   if q is in clicked
    clicked_qs = Post.objects.filter(clicked=True)
    
    print(posts_qs)
    context = {'queryset': posts_qs, 'clicked_list':clicked_qs}
    return render(request, 'company/notification.html', context)


#  this delete the information, should contains the id of the post to delete
# here this method should capture the id of the post to delete
def deleteNotification(request, notification_id=None):
    # lets first get the post object with that id
    if notification_id:
        postToDelete = Post.objects.get(id = notification_id)
        postToDelete.delete()
        return HttpResponseRedirect('/compNotification/') #this will redirect us to another page on success deletion of post object
    else:
        print("The post of that id is not found")
    username = request.user.username

    # kwanza unajua kuwa tukishadelete basi hiyo id inakua haipo tena
    posts_qs = Post.objects.filter(receiver=username).order_by('-created_at')
    if posts_qs.exists():
        context = {'queryset': posts_qs}
    else:
        context = {}
    # here after deleting the element, i think it will fit since that two interface of showing nitifcation and enter inside to view information are relateds
    return render(request, 'company/notification.html', context)
    #return HttpResponseRedirect('/comreceivedOrder/')

# Hapa ndo naona umuhimu wa update view
def realseenotification(request, notification_id):
    exactly_element = Post.objects.get(id=notification_id)
    print(exactly_element)

    exactly_element.clicked = True
    exactly_element.save()

    # lets try dealing with this json data from that i only want to capture the item vs its quantity in dictionary/or in two separate lists, lets try this shit

    head = exactly_element.head
    body = exactly_element.body
    sender= exactly_element.sender
    phone = exactly_element.contact
    zipcode = exactly_element.code
    district = exactly_element.district
    ward = exactly_element.ward
    street = exactly_element.street
    location = exactly_element.physical_address
    itemsAndQuantity = exactly_element.items
    anza = exactly_element.startDate
    maliza = exactly_element.finishDate
    mode = exactly_element.mode
    print(itemsAndQuantity)

    items = []
    quantity = []
    itemsInArray = eval(itemsAndQuantity) # this is used to convert the complex list/json inside the string in the list/json/dict
    noOfElements  = len(itemsInArray)
    associatedCartObj = Cart.objects.get(id=itemsInArray[0]['fields']['cart'])
    totalAmountPayed = associatedCartObj.total
    print("This is the total amount payed by the  customer "+str(totalAmountPayed))
    # then since we said that 15% percent of this amount is for system so lets calculate amount that is for the system and other is paid for the company/laundry when the job is done
    amountAllocatedToSystem = 0.15 * totalAmountPayed
    amountAllocatedToLaundry = int(0.85 * totalAmountPayed)
    print(str(amountAllocatedToLaundry), str(amountAllocatedToSystem))
    for no in range(noOfElements):
        idOfProduct = itemsInArray[no]['fields']['product']
        # remember this id should give us the actual name of the item>> getQuantity with id of given 
        productObj = Product.objects.get(id = idOfProduct)
        productName = productObj.title
        print(productName)
        items.append(productName)
        associatedQuantity = itemsInArray[no]['fields']['quantity']
        quantity.append(associatedQuantity)
    print(str(items))
    print(str(quantity))
    quantityLen = len(quantity)
    sum = 0
    n=0
    for quantity[n] in quantity:
        sum = sum + quantity[n]
        n=+1
    print(str(sum))
    # lets then joins this two lists inside the dictionary, here the prodct name be key and then quantity value,  then we will import both of them key and value, and if there are many of them then we will iterate to produce something

    dictOfBothItemsAndItsCorrespondingQuantity = dict(zip(items, quantity))
    print(str(dictOfBothItemsAndItsCorrespondingQuantity))
    
    # then lets convert this dict in our format 
    # then lets transmit this data from of dict as items, then from this dict will will iterate its value and key, embu create this context dict
    print("This is the subtotal for this product " +str(itemsInArray[0]['fields']['subtotal']))
    context = {'head':head, 'body':body, 'sender':sender, 'phone':phone, 'zipcode':zipcode, 'district':district, 'ward':ward, 'street':street, 'location':location, 'start':anza, 'end':maliza, 'sum':sum, 'items':dictOfBothItemsAndItsCorrespondingQuantity, 'mode':mode, 'amountPayed': amountAllocatedToLaundry, 'total':totalAmountPayed}
    return render(request, 'company/viewNotification.html', context)




class PasswordChangeView(PasswordChangeView):
    form_class = ChangePassword
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'company/successChangePassword.html', {})


class ViewOrders(TemplateView):
    template_name = "company/r_order.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allOrdersByThisUser = Order.objects.filter(assignedTo = self.request.user).order_by('-created_at')
        
        print(str(allOrdersByThisUser))
        context = {}
        if allOrdersByThisUser:
            context['order_qs'] = allOrdersByThisUser  
        else:
            context = {}
        return context


# On this function for letter I should add the logic to deposit the money to the laundryman/company account
def orderCompleted(request, order_id):
    orderObj = Order.objects.get(id=order_id)
    orderObj.order_status = "Completed"
    orderObj.save()
    givenOrderTotal = orderObj.cart.total
    allOrdersByThisUser = Order.objects.filter(assignedTo = request.user).order_by('-created_at')

    # Take this given by total and calculate 0.85 of it for mfuaji while 0.15 for us
    allocatedBalance = int(0.85 * givenOrderTotal)

    # the email associated with the company is given like this

    # get the companies profile where user == request.user
    givenCompany  = companyProfile.objects.get(user=request.user)
    givenCompanyEmail = givenCompany.user.email
    print(givenCompanyEmail)
    # then get the account number of givenCompany
    accNo = givenCompany.account_number
    # get the payment record with given accNo
    associatedPaymentObj = Payment.objects.get(account_number=accNo)
    associatedPaymentObj.balance += allocatedBalance
    associatedPaymentObj.save()
    # remove this allocatedBalance from the fua yako account of '0753752668'
    systemAccountObj = Payment.objects.get(account_number = '0753752668')
    systemAccountObj.balance -= allocatedBalance
    systemAccountObj.save()

    print("Everything works fine amount has been submitted")
    # After everything works fine notify the given laundry/company via email that amount of cash has been deposited to his/her account

    send_mail(
        'Payment completed',
        'The amount of Tshs '+str(allocatedBalance)+ ' has been submitted to your account after completed the  laundry for your customer',
        'mweuc654@gmail.com',
        [givenCompanyEmail],
    )

    # How to get the user email.... We should use order to access the user
    placed_by = orderObj.ordered_by
    associatedEmail = placed_by.email

    send_mail(
        "Order status",
        "Your order has been successful completed, notified by Fua Yako",
        'mweuc654@gmail.com',
        [associatedEmail],
    )
    
    context = {}
    if allOrdersByThisUser:
        context = {'order_qs': allOrdersByThisUser}
    else:
        context= {}
    return render(request, 'company/r_order.html', context)


