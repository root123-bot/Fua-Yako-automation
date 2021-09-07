from django.shortcuts import render, redirect
from .forms import LaundryForm, ChangeProfile
from django.http import HttpResponseRedirect
from .forms import LaundryForm, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from laundryManagementSystem.laundryman.models import LaundryProfile
from laundryManagementSystem.addtocart.models import Post, Cart, Product, Order
from laundryManagementSystem.Payment.models import Payment
from laundryManagementSystem.Payment.forms import PaymentForm
from django.core.mail import send_mail

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = LaundryForm(request.POST)

        if form.is_valid():
            form.save()
            print('Form is saved ')
            return HttpResponseRedirect('/laundry/profile/')

    else:
        form = LaundryForm()
    context = {'form':form}
    return render(request, 'laundryman/index.html', context)
  
def laundrylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('viewprofile/')
        else:
            messages.error(request, 'Incorrent username/password')
    context = {}  
    return render(request, 'laundryman/realLogin.html', context) 


class LaundryProfileView(TemplateView):
    template_name = 'company/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = LaundryProfile.objects.get(user=self.request.user)
  
        wilaya = profile.district
        mkoa = profile.region
        kata = profile.ward
        mtaa = profile.street
        laundry_name = profile.user.username
        email = profile.user.email
        mobile = profile.tele
        pic = profile.photo.url
        anuani = profile.location
  
        context['name'] = laundry_name
        context['region'] = mkoa
        context['district'] = wilaya
        context['ward'] = kata
        context['street'] = mtaa
        context['mobile'] = mobile
        context['pic'] = pic
        context['anuani'] = anuani
        context['email'] = email

        return context
    
def changeProfileForm(request):
    if request.method == 'POST':
        form = ChangeProfile(request.POST, request.FILES)
        user = User.objects.get(username = request.user.username)
        print(user)
        profile = LaundryProfile.objects.get(user=request.user)
        pic = profile.photo.url
        if user and profile:
            if form.is_valid():  
                user.email = form.cleaned_data['email']
                print(user.email)
                user.save()
                profile.photo = form.cleaned_data['profile_picture']
                profile.tele = form.cleaned_data['contact']
                profile.location = form.cleaned_data['location']
                profile.region = form.cleaned_data['region']
                profile.district = form.cleaned_data['district']
                profile.ward = form.cleaned_data['ward']
                profile.street = form.cleaned_data['street']

                profile.save()
                messages.success(request, "Your information has successful updated")
                return HttpResponseRedirect('viewprofile/')
    else: 
        form = ChangeProfile()
        profile = LaundryProfile.objects.get(user=request.user)
        pic = profile.photo.url
    context = {'form':form, 'pic':pic}
    return render(request, 'laundryman/editProfile.html', context)



def profile(request):
    if request.method == 'POST':
        profile_form = Profile(request.POST, request.FILES)
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
            profile.save()
            PaymentObj = Payment.objects.create(username = profile.user.username, password = 'paschal123', account_number = account_numberForm.cleaned_data['account_number'], balance = 0)
            print('Profile form is saved')
            messages.info(request, "You account has been created successful, login here!")
            return HttpResponseRedirect('laundry/login')
    else:
        profile_form = Profile()
        account_numberForm = PaymentForm()
    context = {'profile_form': profile_form, 'accForm':account_numberForm}
    return render(request, 'laundryman/profile.html', context)



def viewNotification(request):
    # When a user click link I want to drag all post information from the database and pass as contex variable to notification link
    # Fist all post records associated with this company
    username = request.user.username
    print(username)
    posts_qs = Post.objects.filter(receiver=username).order_by('-created_at')

    clicked_qs = Post.objects.filter(clicked=True)
    print(posts_qs)
    context = {'queryset': posts_qs, 'clicked_list':clicked_qs}  
    return render(request, 'laundryman/notification.html', context)


def realseelaunotification(request, notification_id):
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
    forDemo = dict(zip(items, quantity))
    print(str(forDemo))
    quantityLen = len(quantity)
    sum = 0
    n=0
    for quantity[n] in quantity:
        sum = sum + quantity[n]
        n=+1
    print(str(sum))
    # lets then joins this two lists inside the dictionary, here the prodct name be key and then quantity value,  then we will import both of them key and value, and if there are many of them then we will iterate to produce something

    # dictOfBothItemsAndItsCorrespondingQuantity = dict(zip(items, quantity))
    # print(str(dictOfBothItemsAndItsCorrespondingQuantity))
    
    # then lets convert this dict in our format 
    # then lets transmit this data from of dict as items, then from this dict will will iterate its value and key, embu create this context dict
    

    print("This is the subtotal for this product " +str(itemsInArray[0]['fields']['subtotal']))
    context = {'head':head, 'body':body, 'sender':sender, 'phone':phone, 'zipcode':zipcode, 'district':district, 'ward':ward, 'street':street, 'location':location, 'start':anza, 'end':maliza, 'sum':sum, 'items':forDemo, 'mode':mode, 'amountPayed': amountAllocatedToLaundry, 'total':totalAmountPayed}
    return render(request, 'laundryman/viewNotification.html', context)

class ViewOrders(TemplateView):
    template_name = "laundryman/r_i_order.html"
    
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
    givenCompany  = LaundryProfile.objects.get(user=request.user)
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
    return render(request, 'laundryman/r_i_order.html', context)