from dotenv import load_dotenv
load_dotenv()

import os

from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from time import time
from django.http import HttpResponse
from pprint import pprint
from paytm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from qr_code.qrcode.utils import QRCodeOptions

User = get_user_model()

# merchant key ( keep it a secret )
MERCHANT_ID = os.environ.get('PAYTM_MERCHANT_ID')
MERCHANT_KEY = os.environ.get('PAYTM_MERCHANT_KEY')

# Create your views here.

@login_required
def homepage(request):
    form = TicketForm()
    amount = 0
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit= False)
            ticket.user = request.user

            active_user = User.objects.get(email = request.user.email)
            
            amount = int(request.POST['no_of_tickets'])*100  # for now price is fixed
            ticket.save()  
        
            cust_id  = 'apneaap'+str(time())+str(ticket.ticket_id)
            
            print(" ticket  id : ",ticket.ticket_id)
            print("customer id :" ,cust_id)
            print("mobile number : " , active_user.mobile_number)
            print(" Email : " ,active_user.email)

            paytmParams = {
                "MID" : MERCHANT_ID,
                "WEBSITE" : "WEBSTAGING",
                "INDUSTRY_TYPE_ID" : "Retail",
                "CHANNEL_ID" : "WEB",
                "ORDER_ID" : str(ticket.ticket_id),
                "CUST_ID" : cust_id,
                "EMAIL" : request.user.email,
                "TXN_AMOUNT" : "{0:.2f}".format(amount),
                "CALLBACK_URL" : "http://localhost:8000/qrcode/",
            }
            if active_user.mobile_number :
                paytmParams["MOBILE_NO"]= str(active_user.mobile_number)
            
            checksum = Checksum.generate_checksum(paytmParams, MERCHANT_KEY)
            print("Checksum Generated ....... "+checksum + '\n')
            
            paytmParams["CHECKSUMHASH"] = checksum 

            pprint(dict(paytmParams))

            return render(request , 'booking/paytm.html',{'param_dict' : paytmParams})

    return render( request, 'booking/homepage.html',{'form':form ,'amount':amount})

@csrf_exempt
def qrcode(request):
    print("Payment request received!! \n")
    pprint(dict(request.POST))
    
    form = request.POST 
    paytmChecksum = ""
    paytmParams = {}
    for key, value in form.items(): 
        if key == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key] = value

    if paytmChecksum == "" :
        raise ValueError("You are a fraud!!!!")

    # Verify checksum
    isValidChecksum = Checksum.verify_checksum(paytmParams, MERCHANT_KEY, paytmChecksum)
    if isValidChecksum:
        print("Checksum Matched")
    else:
        print("Checksum Mismatched")
    
    if paytmParams['RESPCODE'] != '01':
        return HttpResponse("Payment not successful!!!!")

    ticket = Ticket.objects.get(ticket_id = paytmParams['ORDERID'])

    message = {
        'boarding_station':ticket.boarding_station_code,
        'destination_station':ticket.destination_station_code,
        'no_of_tickets' : ticket.no_of_tickets ,
    }

    context = dict( my_options = QRCodeOptions(size = 'm', version = '5' ,image_format = "png"), message = message )
    return render(request,'booking/qrcode.html',context=context )
