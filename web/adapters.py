from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("ADAPTER RUNNING")

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            request.session["existing_user"] = True
        else:
            request.session["existing_user"] = False

    def get_login_redirect_url(self, request):
        if request.session.get("existing_user"):
            return reverse("home")

        return reverse("createroom")