from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django.contrib.auth import login,logout,authenticate
import random

# from django.http import HttpResponse, JsonResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
#
# from django.http import HttpResponse
# import requests
# from requests.auth import HTTPBasicAuth
# import json
# from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
#
#
# def getAccessToken(request):
#     consumer_key = 'XJOD78XsSN9GYrBTuPJhtlySmwna21zo'
#     consumer_secret = 'oOE7NuQeXYu7DTJl'
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#
#     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#
#     return HttpResponse(validated_mpesa_access_token)
#
#
# def lipa_na_mpesa_online(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = {
#         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#         "Password": LipanaMpesaPpassword.decode_password,
#         "Timestamp": LipanaMpesaPpassword.lipa_time,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 1,
#         "PartyA": 254701628981,  # replace with your phone number to get stk push
#         "PartyB": LipanaMpesaPpassword.Business_short_code,
#         "PhoneNumber": 254701628981,  # replace with your phone number to get stk push
#         "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
#         "AccountReference": "Henry",
#         "TransactionDesc": "Testing stk push"
#     }
#     response = requests.post(api_url, json=request, headers=headers)
#     return HttpResponse('success')
#
#
# @csrf_exempt
# def register_urls(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
#                "ResponseType": "Completed",
#                "ConfirmationURL": "https://bcb733b45166.ngrok.io/Ecommerce/c2b/confirmation",
#                "ValidationURL": "https://bcb733b45166.ngrok.io/Ecommerce/c2b/validation"}
#     response = requests.post(api_url, json=options, headers=headers)
#     return HttpResponse(response.text)
#
#
# @csrf_exempt
# def call_back(request):
#     pass
#
#
# @csrf_exempt
# def validation(request):
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))
#
#
# @csrf_exempt
# def confirmation(request):
#     mpesa_body =request.body.decode('utf-8')
#     mpesa_payment = json.loads(mpesa_body)
#     payment = MpesaPayment(
#         first_name=mpesa_payment['FirstName'],
#         last_name=mpesa_payment['LastName'],
#         middle_name=mpesa_payment['MiddleName'],
#         description=mpesa_payment['TransID'],
#         phone_number=mpesa_payment['MSISDN'],
#         amount=mpesa_payment['TransAmount'],
#         reference=mpesa_payment['BillRefNumber'],
#         organization_balance=mpesa_payment['OrgAccountBalance'],
#         type=mpesa_payment['TransactionType'],
#     )
#     payment.save()
#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))
#
#
#
#
#


def about(request):
    return render(request, 'Ecommerce/about_us.html')


def mpesa_deposit(request):
    return render(request, 'Ecommerce/mpesa_deposit.html')


def transaction_log(request):
    return render(request, 'Ecommerce/transaction_log.html')


def profile(request):
    user = User.objects.filter(pk=request.user.id)
    context = {
        'users': user,
    }
    return render(request, 'Ecommerce/profile.html', context)


def investment(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'User is not authenticated.')
        return redirect('Ecommerce:login')
    else:
        return render(request, 'Ecommerce/investment.html')


def stock_summary(request):
    all_stock = Item.objects.all()
    context = {
        'all_stock': all_stock
    }
    return render(request, 'Ecommerce/item_collection.html', context)


def toggleactivate(request,item_id):
    item = Item.objects.get(pk=item_id)
    item.ShowCastToCustomers = not item.ShowCastToCustomers
    item.save()
    if item.ShowCastToCustomers is True:
        messages.info(request, 'Item Activated.')
    else:
        messages.warning(request, 'Item hidden.')
    return redirect('Ecommerce:stock_summary')


class HomeView(ListView):
    model = Item
    queryset = Item.objects.filter(ShowCastToCustomers=True)
    paginate_by = 8
    template_name = 'Ecommerce/home-page.html'


def add_stock(request):
    if request.user.username != 'admin':
        return redirect('Ecommerce:home')
    else:
        form=AddStockForm()
        if request.method == 'POST':
            form = AddStockForm(request.POST or None, request.FILES or None)
            print(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                title = form.cleaned_data.get('title')

                slid = random.randint(0, 100)
                item.image = request.FILES['image']
                item.slug = title.replace(' ','-')+'-'+str(slid)
                item.save()
                print('form is valid')

                messages.success(request, 'Item Added Successfully')
                return redirect('Ecommerce:home')
            else:
                messages.warning(request, 'Invalid URL try again.')
                context = {
                    'form': form,
                }
                return render(request, 'Ecommerce/Add_items.html', context)

        context = {
            'form': form,
        }
        return render(request, 'Ecommerce/Add_items.html', context)


def edit_item(request, item_id):
    if request.user.username != 'admin':
        return redirect('Ecommerce:home')
    else:
        item = Item.objects.get(pk=item_id)
        form = AddStockForm(instance=item)

        if request.method == 'POST':
            form = AddStockForm(request.POST, request.FILES or None, instance=item,)
            if form.is_valid():
                item.image = request.FILES['image']
                form.save()
                messages.success(request, 'Update Successful')
                return redirect('Ecommerce:stock_summary')
        context = {
            'title': 'Edit',
            'form': form,
        }
        return render(request, 'Ecommerce/edit_items.html', context)


def delete_item(request, item_id):
    if request.user.username != 'admin':
        return redirect('Ecommerce:home')
    else:

        item = Item.objects.get(pk=item_id)
        item.delete()
        messages.success(request, 'Delete Successful.')
        return redirect('Ecommerce:stock_summary')

@receiver(post_save, sender=MpesaPayment)
def update_wallet(sender, instance, created, **kwargs):
    try:
        if created:
           wallet= Wallet.objects.get(
                user_name=instance.phone_number,
            )
           wallet.available_balance+=instance.amount
           wallet.save()
    except ObjectDoesNotExist:
        return redirect('Ecommerce:investment')


@receiver(post_save, sender=User)
def create_wallet(sender,instance,created,**kwargs):
    if created:
        Wallet.objects.create(
            user_name=instance.username
        )























#
#
# class OrderSummary(View):
#     def get(self, *args, **kwargs):
#
#         try:
#             order = Order.objects.get(
#                 user=self.request.user,
#                 ordered=False
#             )
#             context = {
#                 'object': order
#             }
#             return render(self.request, 'Ecommerce/investment.html', context)
#         except ObjectDoesNotExist:
#             messages.warning(self.request, 'You do not have an active order.')
#             return redirect('Ecommerce:home')
#
#
# class ProductView(DetailView):
#     model = Item
#     template_name = 'Ecommerce/transaction_log.html'
#
#
# def add_to_cart(request, slug):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'You must sign in to Item add to cart')
#         return redirect('Ecommerce:product', slug=slug)
#     else:
#         item = get_object_or_404(Item, slug=slug)
#         order_item, created = OrderItem.objects.get_or_create(
#             item=item,
#             user=request.user,
#             ordered=False
#         )
#         order_qs = Order.objects.filter(
#             user=request.user,
#             ordered=False
#         )
#         if order_qs.exists():
#             order = order_qs[0]
#             if order.items.filter(item__slug=item.slug).exists():
#                 order_item.quantity += 1
#                 order_item.save()
#                 messages.info(request, 'Item Quantity successfully updated.')
#                 return redirect("Ecommerce:product", slug=slug)
#
#             else:
#                 messages.info(request, 'Item Added to Cart')
#                 order.items.add(order_item)
#                 return redirect("Ecommerce:product", slug=slug)
#
#         else:
#             ordered_date = timezone.now()
#             order = Order.objects.create(
#                 user=request.user,
#                 ordered_date=ordered_date,
#             )
#             order.items.add(order_item)
#             messages.info(request, 'Item was Added to your Cart.')
#
#         return redirect("Ecommerce:product", slug=slug)
#
#
# def add_single_item_to_cart(request, slug):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'You must sign in to Item add to cart')
#         return redirect('Ecommerce:product', slug=slug)
#     else:
#         item = get_object_or_404(Item, slug=slug)
#         order_item, created = OrderItem.objects.get_or_create(
#             item=item,
#             user=request.user,
#             ordered=False
#         )
#         order_qs = Order.objects.filter(
#             user=request.user,
#             ordered=False
#         )
#         if order_qs.exists():
#             order = order_qs[0]
#             if order.items.filter(item__slug=item.slug).exists():
#                 order_item.quantity += 1
#                 order_item.save()
#                 messages.info(request, 'Item Quantity successfully updated.')
#                 return redirect("Ecommerce:order_summary")
#
#             else:
#                 messages.info(request, 'Item Added to Cart')
#                 order.items.add(order_item)
#                 return redirect("Ecommerce:order_summary")
#
#         else:
#             ordered_date = timezone.now()
#             order = Order.objects.create(
#                 user=request.user,
#                 ordered_date=ordered_date,
#             )
#             order.items.add(order_item)
#             messages.info(request, 'Item was Added to your Cart.')
#
#         return redirect("Ecommerce:order_summary")
#
#
# def remove_from_cart(request, slug):
#     if not request.user.is_authenticated:
#         messages.warning(request, 'You must sign in to Item remove item from cart')
#         return redirect('Ecommerce:product', slug=slug)
#     else:
#         item = get_object_or_404(Item, slug=slug)
#         order_qs = Order.objects.filter(
#             user=request.user,
#             ordered=False
#         )
#         if order_qs.exists():
#             order = order_qs[0]
#             if order.items.filter(item__slug=item.slug).exists():
#                 order_item = OrderItem.objects.filter(
#                     user=request.user,
#                     ordered=False,
#                     item=item,
#
#                 )[0]
#                 order_item.quantity = 1
#                 order_item.save()
#                 order.items.remove(order_item)
#                 messages.info(request, 'Item was removed From your Cart.')
#                 return redirect('Ecommerce:order_summary')
#             else:
#                 messages.info(request, 'Item is not in your cart.')
#                 return redirect('Ecommerce:product', slug=slug)
#         else:
#             messages.info(request, 'You do not have an active order.')
#             return redirect('Ecommerce:product', slug=slug)
#
#
# def remove_single_item_from_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_qs = Order.objects.filter(
#         user=request.user,
#         ordered=False
#     )
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item = OrderItem.objects.filter(
#                 user=request.user,
#                 ordered=False,
#                 item=item,
#
#             )[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#             else:
#                 order.items.remove(order_item)
#             messages.info(request, 'This item quantity was updated.')
#             return redirect('Ecommerce:order_summary')
#         else:
#             messages.info(request, 'Item is not in your cart.')
#             return redirect('Ecommerce:product', slug=slug)
#     else:
#         messages.info(request, 'You do not have an active order.')
#         return redirect('Ecommerce:product', slug=slug)
#
#
# class CheckoutView(View):
#
#     def get(self,*args,**kwargs):
#         if not self.request.user.is_authenticated:
#             messages.warning(self.request, 'Authorized page!')
#             return redirect('Ecommerce:login')
#         else:
#             try:
#                 form = CheckoutForm()
#                 order = Order.objects.get(user=self.request.user, ordered=False)
#
#                 context = {
#                     'form': form,
#                     'order': order,
#                 }
#                 return render(self.request, 'Ecommerce/about_us.html', context)
#             except ObjectDoesNotExist:
#                 messages.warning(self.request, 'You do not have an active Order.')
#                 return redirect('Ecommerce:home')
#
#     def post(self, *args,**kwargs):
#         if not self.request.user.is_authenticated:
#             messages.warning(self.request, 'Authorized page!')
#             return redirect('Ecommerce:login')
#         else:
#             form = CheckoutForm(self.request.POST or None)
#             try:
#                 order= Order.objects.get(user=self.request.user,ordered=False)
#                 if form.is_valid():
#                     street_name = form.cleaned_data.get('street_name')
#                     apartment_address = form.cleaned_data.get('apartment_address')
#                     country = form.cleaned_data.get('country')
#                     zip = form.cleaned_data.get('zip')
#                     # same_billing_address = form.cleaned_data.get('same_billing_address')
#                     save_info = form.cleaned_data.get('save_info')
#                     # payment_option = form.cleaned_data.get('payment_option')
#
#                     address = Address(
#                         user=self.request.user,
#                         street_name=street_name,
#                         apartment_address=apartment_address,
#                         country=country,
#                         zip=zip,
#                         default=save_info,
#                         # same_billing_address=same_billing_address,
#                         # save_info=save_info,
#                     )
#                     print(form.cleaned_data)
#                     address.save()
#                     order.billing_address = address
#                     order.save()
#                     messages.info(self.request, 'Successful checkout')
#                     return redirect('Ecommerce:payment')
#                 print(form.cleaned_data)
#
#             except ObjectDoesNotExist:
#                 messages.error(self.request, 'You do not have an Active order.')
#                 return redirect('Ecommerce:home')
#
#
# class PaymentView(View):
#
#     def get(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             messages.warning(self.request, 'Authorized page!')
#             return redirect('Ecommerce:login')
#         else:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'order':order
#             }
#             return render(self.request, 'Ecommerce/payment.html', context)
#
#     def post(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             messages.warning(self.request, 'Authorized page!')
#             return redirect('Ecommerce:login')
#         else:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             amount = order.get_total()
#             payment = Payment()
#             payment.stripe_charge_id = self.request.user
#             payment.user = self.request.user
#             payment.amount = amount
#             payment.save()
#
#             order_items = order.items.all()
#             order_items.update(ordered=True)
#             for item in order_items:
#                 item.save()
#             order.ordered = True
#             order.payment = payment
#             order.save()
#             messages.success(self.request, 'Order was Successful')
#             return redirect('Ecommerce:home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in Successfully as ' + request.user.username)
                return redirect('Ecommerce:home')
            else:
                messages.warning(request, 'Account is locked. Contact Administrator.')
                return render(request, 'Ecommerce/login.html')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return render(request, 'Ecommerce/login.html')
    return render(request, 'Ecommerce/login.html')


def register(request):
    if request.method == 'POST':
        form = UserLogForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Signed Up successfully as ' + request.user.username)
                    return redirect('Ecommerce:home')
        context = {
            'form': form,
        }
        messages.warning(request, 'Error. Username already Taken Try another.')
        return render(request, 'Ecommerce/register.html', context)
    else:
        form = UserLogForm(request.POST or None)
        context = {
            'form':form,
        }
        return render(request, 'Ecommerce/register.html', context)


def logout_user(request):
    logout(request)
    form = UserLogForm(request.POST or None)
    context = {
        'form': form
    }
    messages.success(request, 'Successfully Logged out.')
    return redirect(reverse('Ecommerce:login'), context)

