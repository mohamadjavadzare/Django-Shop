from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_password_reset_email  # تابع Celery برای ارسال ایمیل

from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .models import Profile

from django.views.generic.edit import FormView
from .forms import CustomUserCreationForm  # فرم ثبت‌نام
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Profile
from django.db import IntegrityError


class RegisterView(FormView):
    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        try:
            user = form.save()  # ذخیره کاربر جدید
            
            # بررسی وجود پروفایل
            if not hasattr(user, 'user_profile'):
                Profile.objects.create(user=user)  # ایجاد پروفایل برای کاربر جدید
            
            login(self.request, user)  # ورود کاربر جدید
            messages.success(self.request, "ثبت‌نام با موفقیت انجام شد!")  # پیام موفقیت
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, "خطا در ایجاد حساب کاربری. لطفاً دوباره تلاش کنید.")  # پیام خطا
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "لطفاً فرم را به درستی پر کنید.")  # پیام خطا در صورت نامعتبر بودن فرم
        return super().form_invalid(form)
    

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass



from django.utils.translation import gettext_lazy as _

class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/reset-password.html"
    email_template_name = "accounts/reset-password-email.html"
    subject_template_name = "accounts/reset-password-subject.txt"
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user_generator = form.get_users(email)  # ایجاد generator برای کاربران

        try:
            user = next(user_generator)  # دریافت اولین کاربر از generator
            subject = render_to_string(self.subject_template_name)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string(self.email_template_name, {
                'email': user.email,
                'domain': self.request.get_host(),
                'uid': uid,
                'token': token,
            })
            # ارسال ایمیل به صورت غیرهمزمان
            send_password_reset_email.delay(subject, message, settings.EMAIL_HOST_USER, [user.email])
            messages.success(self.request, _("لینک بازنشانی رمز عبور به ایمیل شما ارسال شد."))
        except StopIteration:
            messages.error(self.request, _("کاربری با این ایمیل پیدا نشد."))

        return super().form_valid(form)



class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/reset-password-confirm.html"
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/reset-password-done.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/reset-password-complete.html"
