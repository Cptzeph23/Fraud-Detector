import os, json, requests, base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Transaction, FraudAlert
from . import ml
from datetime import datetime
DARJA_TOKEN_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
DARJA_STK_PUSH_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
def get_daraja_access_token():
    key = os.getenv('DARJA_CLIENT_KEY')
    secret = os.getenv('DARJA_CLIENT_SECRET')
    r = requests.get(DARJA_TOKEN_URL, auth=(key, secret))
    if r.status_code == 200:
        return r.json().get('access_token')
    raise RuntimeError('Daraja token error: ' + r.text)
def send_gava_sms(phone, message):
    api_url = os.getenv('GAVA_API_URL')
    headers = {'Authorization': f'Bearer {os.getenv("GAVA_API_KEY")}', 'Content-Type':'application/json'}
    payload = {'phone': phone, 'message': message}
    try:
        r = requests.post(api_url, json=payload, headers=headers, timeout=10)
        return r.status_code in (200,201)
    except Exception:
        return False
def compute_features(amount, phone, merchant_id):
    # IMPORTANT: Replace with real feature extraction matching your training features.
    # Example assumes model expects ['V1',...,'V28','NormalizedAmount'] - here we set zeros.
    features = {}
    for i in range(1,29):
        features[f'V{i}'] = 0.0
    features['NormalizedAmount'] = float(amount)
    return features
def decide_action(prob, threshold=0.5):
    return 'FLAG' if prob >= threshold else 'ALLOW'
@require_POST
def create_transaction(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        phone = data.get('phone')
        amount = data.get('amount')
        merchant_id = data.get('merchant_id','')
        features = compute_features(amount, phone, merchant_id)
        prob = ml.predict(features)
        status = 'PENDING'
        if decide_action(prob) == 'FLAG':
            status = 'FLAGGED'
        tx = Transaction.objects.create(phone_number=phone, amount=amount, merchant_id=merchant_id, features_json=features, fraud_probability=prob, status=status)
        if status == 'FLAGGED':
            msg = f'Suspicious transaction flagged for KES {amount}. Our team will contact you.'
            FraudAlert.objects.create(transaction=tx, message=msg)
            send_gava_sms(phone, msg)
            return JsonResponse({'transaction_id': tx.id, 'status': 'FLAGGED', 'fraud_probability': prob})
        # Initiate Daraja STK Push for allowed transactions
        token = get_daraja_access_token()
        shortcode = os.getenv('DARJA_SHORTCODE')
        passkey = os.getenv('DARJA_PASSKEY')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = shortcode + passkey + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode()
        payload = {
            'BusinessShortCode': shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(float(amount)),
            'PartyA': phone,
            'PartyB': shortcode,
            'PhoneNumber': phone,
            'CallBackURL': os.getenv('DARJA_CALLBACK_URL'),
            'AccountReference': f'TX{tx.id}',
            'TransactionDesc': 'Payment'
        }
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.post(DARJA_STK_PUSH_URL, json=payload, headers=headers, timeout=15)
        if r.status_code in (200,201):
            resp = r.json()
            tx.mpesa_checkout_request_id = resp.get('CheckoutRequestID') or ''
            tx.save()
            return JsonResponse({'transaction_id': tx.id, 'status': 'PENDING', 'fraud_probability': prob})
        else:
            tx.status = 'FAILED'; tx.save()
            return JsonResponse({'error': 'Daraja push failed', 'details': r.text}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def daraja_callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        body = data.get('Body',{})
        stk = body.get('stkCallback',{})
        checkout_request_id = stk.get('CheckoutRequestID')
        result_code = stk.get('ResultCode')
        result_desc = stk.get('ResultDesc')
        try:
            tx = Transaction.objects.get(mpesa_checkout_request_id=checkout_request_id)
        except Transaction.DoesNotExist:
            return HttpResponse(status=404)
        if result_code == 0:
            tx.status = 'SUCCESS'
            tx.save()
            send_gava_sms(tx.phone_number, f'Payment of KES {tx.amount} succeeded. Thank you.')
        else:
            tx.status = 'FAILED'; tx.save()
            send_gava_sms(tx.phone_number, f'Payment failed: {result_desc}')
        return JsonResponse({'status':'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def dashboard(request):
    total = Transaction.objects.count()
    flagged = Transaction.objects.filter(status='FLAGGED').count()
    success = Transaction.objects.filter(status='SUCCESS').count()
    failed = Transaction.objects.filter(status='FAILED').count()
    recent = Transaction.objects.order_by('-created_at')[:10]
    return render(request, 'transactions/dashboard.html', {'total':total,'flagged':flagged,'success':success,'failed':failed,'recent':recent})
def transaction_form(request):
    return render(request, 'transactions/transaction_form.html')
def alerts(request):
    alerts = FraudAlert.objects.order_by('-created_at')[:50]
    return render(request, 'transactions/alerts.html', {'alerts': alerts})

def index(request):
    return render(request, 'transactions/index.html')

