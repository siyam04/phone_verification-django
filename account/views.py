from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from .forms import PhoneNumberForm, CheckOtpForm, GetPasswordForm, UserLoginForm
from .models import PhoneRegistration
import re, random

# Create your views here.

global CHEC_OTP
CHEC_OTP = False

def is_phone_valid(phone_number):
    if phone_number:
        MOBILE_REGEX = re.compile('^(?:\+?88)?01[15-9]\d{8}$')
        if MOBILE_REGEX.match(phone_number):
            return True
        else:
            return False
    else:
        return False

def generate_otp():
    otp = random.sample(range(10**(6-1), 10**6), 1)[0]
    return otp

def get_phone_number(request):
    print('working')
    if request.method == 'POST':
        forms = PhoneNumberForm(request.POST)
        if forms.is_valid():
            phone_number = forms.cleaned_data['phone_number']
            if is_phone_valid(phone_number):
                try:
                    User.objects.get(username=phone_number)
                    context = {
                        'forms': forms,
                        'errMsg': 'User with this phone number already exits.'
                    }
                    template = 'account/get_phone_number.html'
                    return render(request, template, context)
                except:
                    pass

                otp = generate_otp()
                request.session['phone_number'] = phone_number
                request.session['otp_code'] = otp

                try:
                    obj = PhoneRegistration.objects.get(phone_number=phone_number)
                    obj.otp_code = otp
                    obj.save()
                except ObjectDoesNotExist:
                    PhoneRegistration.objects.create(phone_number=phone_number, otp_code=otp)

                return redirect('check-otp')
            else:
                context = {
                    'forms': forms,
                    'errMsg': 'Invalid Phone Number. Insert a valid Phone Number.'
                }
                template = 'account/get_phone_number.html'
                return render(request, template, context)

    forms = PhoneNumberForm()
    context = {'forms': forms}
    template = 'account/get_phone_number.html'
    return render(request, template, context)


def check_otp(request):
    phone_number = request.session['phone_number']
    otp_code = PhoneRegistration.objects.get(phone_number=phone_number)

    if request.method == 'POST':
        otp_form = CheckOtpForm(request.POST)
        if otp_form.is_valid():
            phone_number = request.session['phone_number']
            otp_code = otp_form.cleaned_data['otp_code']
            try:
                obj = PhoneRegistration.objects.get(phone_number=phone_number, otp_code=otp_code, otp_passed=False)
                obj.otp_passed = True
                obj.save()
                return redirect('get-password')
            except:
                context = {
                'errMsg': 'Invalid Otp',
                'forms': CheckOtpForm()
                }
                template = 'account/get_password.html'
                return render(request, template, context)

    context = {
        'forms': CheckOtpForm(),
        'otp_code': otp_code.otp_code
    }
    template = 'account/check_otp.html'
    return render(request, template, context)


def get_password(request):
    if request.method == 'POST':
        form = GetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            phone_number = request.session['phone_number']
            otp_code = request.session['otp_code']

            if password == re_password:
                if not PhoneRegistration.objects.filter(phone_number = phone_number, otp_code=otp_code, otp_passed=True).exists():
                    context = {
                        'errMsg': 'Failed! Try again.',
                        'forms': GetPasswordForm()
                    }
                    template = 'account/get_password.html'
                    return render(request, template, context)
                try:
                    User.objects.create_user(username=phone_number, password=password)
                    user = authenticate(request, username=phone_number, password=password)
                    login(request, user)
                    return redirect('home')
                except Exception as e:
                    context = {
                        'errMsg': 'Failed! Try again.',
                        'forms': GetPasswordForm()
                    }
                    template = 'account/get_password.html'
                    return render(request, template, context)
            else:
                context = {
                    'errMsg': "Password doesn't match.",
                    'forms': GetPasswordForm()
                }
                template = 'account/get_password.html'
                return render(request, template, context)

    context = {
        'forms': GetPasswordForm()
    }
    template = 'account/get_password.html'
    return render(request, template, context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = authenticate(request, username=phone_number, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context = {
                    'forms': form,
                    'errMsg': "Phone number or password doesn't match."
                }
                template = 'account/login.html'
                return render(request, template, context)

    form = UserLoginForm()
    context = {'forms': form}
    template = 'account/login.html'
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return redirect('home')
