from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP
from .forms import SignupForm, OTPForm, LoginForm
from django.views.decorators.cache import never_cache
from django.utils import timezone
from datetime import timedelta



# Create your views here.
@never_cache
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signup_data = form.cleaned_data
            email = signup_data['email']

            # create or update OTP record for this email
            otp_obj, _ = OTP.objects.get_or_create(email=email, user=None)
            code = otp_obj.generate_code()

            # store signup data + OTP id in session
            request.session['signup_data'] = signup_data
            request.session['otp_id'] = otp_obj.id

            # send email
            send_mail(
                "wlcome to Hidayathulla's Test website"
                "Your OTP Code",
                f"Your verification code is {code}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "We sent you an OTP to verify your email.")
            return redirect('verify_otp')
    else:
        form = SignupForm()
    
    return render(request, 'User_Signup.html', {'form': form})

@never_cache
def verify_otp_view(request):
    signup_data = request.session.get('signup_data')
    otp_id = request.session.get('otp_id')

    if not signup_data or not otp_id:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect('signup')

    otp_obj = OTP.objects.get(id=otp_id)

    # 🚫 If locked for 2 hours
    if otp_obj.is_locked():
        messages.error(request, "Too many attempts. Please try again after 2 hours.")
        return redirect('signup')

    # ⏱ Resend available time = 1 min after last OTP
    resend_available_at = otp_obj.created_at + timedelta(minutes=1)
    resend_available_at_ts = int(resend_available_at.timestamp() * 1000)  # for JS countdown

    if request.method == "POST":
        if "resend" in request.POST:
            # Check if resend is allowed yet
            if timezone.now() < resend_available_at:
                messages.error(request, "Please wait before requesting another OTP.")
                return redirect('verify_otp')

            # Check resend count
            if otp_obj.resend_count >= 3:
                otp_obj.lock_for_2_hours()
                messages.error(request, "Too many resend attempts. Please try again after 2 hours.")
                return redirect('signup')

            new_code = otp_obj.generate_code()
            otp_obj.resend_count += 1
            otp_obj.save()

            send_mail(
                "Your New OTP Code",
                f"Your new verification code is {new_code}",
                settings.EMAIL_HOST_USER,
                [otp_obj.email],
                fail_silently=False,
            )
            messages.success(request, "We sent you a new OTP. Please check your email.")
            return redirect('verify_otp')

        form = OTPForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['otp']

            if otp_obj.is_expired():
                messages.error(request, "OTP expired. Please request a new one.")
                return redirect('verify_otp')

            if entered_code == otp_obj.code:
                user = User.objects.create_user(
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=signup_data['password1']
                )
                user.is_active = True
                user.save()

                otp_obj.user = user
                otp_obj.is_verified = True
                otp_obj.save()

                del request.session['signup_data']
                del request.session['otp_id']

                messages.success(request, "Email verified! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP. Try again.")
    else:
        form = OTPForm()

    return render(request, "verify_otp.html", {
        "form": form,
        "resend_available_at_ts": resend_available_at_ts,
        "resend_count": otp_obj.resend_count,
    })

@never_cache
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@never_cache
def home_view(request):
    return render(request, "home.html")

@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')



