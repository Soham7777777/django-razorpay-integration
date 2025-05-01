from typing import cast
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from razorpay import Client
import razorpay


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', dict(key_id=settings.RAZORPAY_KEY_ID))


def create_order(request: HttpRequest) -> HttpResponse:
    amount = 500  # Amount in paise (e.g., ₹5)
    currency = 'INR'
    order_data = {
        'amount': amount,
        'currency': currency
    }
    client = cast(Client, settings.RAZORPAY_CLIENT)
    razorpay_order = client.order.create(data=order_data)
    return JsonResponse({'order_id': razorpay_order['id'], 'amount': amount})


def payment_success(request: HttpRequest) -> HttpResponse:
    return render(request, 'success.html')


@csrf_exempt
def verify_signature(request: HttpRequest) -> HttpResponse:
    # Data from Razorpay Checkout
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')

    # Verify signature
    client = cast(Client, settings.RAZORPAY_CLIENT)
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        return redirect('payment_success')  # Redirect to success page
    except razorpay.errors.SignatureVerificationError:
        raise BadRequest('Signature verification failed')
