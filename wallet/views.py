from django.shortcuts import render, redirect
from userdetail.models import *
from cartnew.models import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
import razorpay
import datetime
razorpay_id = "rzp_test_9joF0fVvCUMOZC"
razorpay_secret = "2Alnr3lLV7jsMJ4OJya2eUeO"


# Create your views here.
def wallet(request):
    if request.user.is_authenticated:
        currUser = detail.objects.get(email=request.user.email)
        obj = user_wallet.objects.filter(user=currUser)
        print("***********wallet************",obj)
        if not obj:
            wallet = user_wallet(user=currUser)
            wallet.save()
        return render(request, "wallet/wallet.html", {'obj': obj})
    else:
        return redirect('login_page')

@csrf_exempt
def addmoney(request):
    if request.method == "POST" and 'paytmbutton' in request.POST:
        MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'
        money = request.POST.get('amount')
        currUser = detail.objects.filter(email=request.user.email).first()
        currWallet=user_wallet.objects.filter(user=currUser).first()
        phonenumber = request.POST.get('phonenumber')
        obj = wallet_transaction(wallet=currWallet, amount=money, payment_method="paytm")
        obj.save()
        

        doneorder = True
        id = obj.id
        host = "http://"+request.META['HTTP_HOST']+"/handlerequest/"

        param_dict = {
            'MID': 'LaxLMj03444256041341',
            'ORDER_ID': str(id),
            'TXN_AMOUNT': str(money),
            'CUST_ID': currUser.email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': host,  # payment successfull msg by paytm
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)

        if request.user.is_authenticated:
            return render(request, 'checkout/paytm.html', {'param_dict': param_dict})

        else:
            return redirect('login_page')

    elif request.method == "POST" and 'razorbutton' in request.POST:
        MERCHANT_KEY = 'ewNvWo7IsK3#qZSA'
        money = request.POST.get('amount')
        currUser = detail.objects.filter(email=request.user.email).first()
        currWallet=user_wallet.objects.filter(user=currUser).first()
        phonenumber = request.POST.get('phonenumber')

        doneorder = True
        # id = order.order_id
        # return render(request, 'checkout.html')

        name = currUser.name
        phone = currUser.contact
        address = currUser.address
        email = request.user.email
        # address=""
        context = {}
        context['price'] = int(money)
        # print("amount:::",amount)
        context['name'] = name
        context['phone'] = phone
        context['email'] = email
        context['address'] = address
        order_currency = 'INR'
        order_receipt = datetime.datetime.now()
        order_receipt = order_receipt.strftime("%b%d%y%H%I%p")
        notes = {
            'Shipping address': 'Bommanahalli, Bangalore'}
        client = razorpay.Client(auth=(razorpay_id, razorpay_secret))   
        orderDict = {'amount': int(money)*100, "currency" : order_currency, "receipt" : order_receipt, "notes": notes, "payment_capture": "1"}
        orderResp = client.order.create(orderDict)
        print("orderResp",orderResp)
        order_id = orderResp['id']
        context['order_id'] = order_id
        order_status = orderResp['status']

        if order_status == 'created':
            obj = wallet_transaction(wallet=currWallet, transaction_amount=float(money), payment_method="razorpay", receiving_user=currUser)
            obj.razorpay_order_id = order_id
            obj.save()

            if request.user.is_authenticated:
                return render(request, 'wallet/confirm_order.html', context)
            else:
                return redirect('login_page')
    else:
        return render(request, 'wallet/add_money.html', {})

def checkPaymentStatus(request):
    currUser = detail.objects.filter(email=request.user.email).first()
    currWallet=user_wallet.objects.filter(user=currUser).first()
    if request.method == "POST":
        obj = wallet_transaction.objects.filter(razorpay_order_id=request.POST.get('razorpay_order_id')).first()
        print(f'THIS IS POST {request.POST}')
        razorpay_secret = "2Alnr3lLV7jsMJ4OJya2eUeO"
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature,
        }
        print("hellooooooooo",params_dict)
        razorData = {'razorpay_payment_id':razorpay_payment_id, 'razorpay_order_id':razorpay_order_id, 'razorpay_signature':razorpay_signature}
        client = razorpay.Client(auth=(razorpay_payment_id, razorpay_secret))
        client.utility.verify_payment_signature(razorData)
        obj.razorpay_payment_id = razorpay_payment_id
        obj.is_successful = True
        obj.transaction_status = "SUCCESSFUL"
        obj.save()
        currWallet.amount = currWallet.amount + obj.transaction_amount
        currWallet.save()
        return redirect('wallet')

@csrf_exempt
def sendmoney(request):
    if request.method == "POST":
        currUser = detail.objects.filter(email=request.user.email).first()
        currWallet=user_wallet.objects.filter(user=currUser).first()
        money = request.POST.get('amount')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('emailreciever')
        receiver = detail.objects.get(email=email) 
        obj = wallet_transaction(wallet=currWallet,transaction_amount=float(money), receiving_user=receiver, transactionType="Deduct")
        if currWallet.amount >= obj.transaction_amount:
            currWallet.amount=currWallet.amount - obj.transaction_amount
            currWallet.save()
            obj.transaction_status = "SUCCESSFUL"
            obj.payment_method = "Wallet"
            obj.is_successful = True
            obj.save()

        return redirect('wallet')

    else:
        return render(request, 'wallet/send_money.html', {})