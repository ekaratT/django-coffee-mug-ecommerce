import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY



@csrf_exempt
def stripe_webhook(request):
    # event = stripe.Event.retrieve("evt_1Nr01uCvrtDJk48qRfivDvWT",)
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # The signature verification failed
        return HttpResponse(status=400)
    if event.type ==  'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.is_paid = True
            # Store stripe payment id
            order.stripe_id = session.payment_intent
            order.save()
    return HttpResponse(status=200)