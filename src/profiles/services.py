from django.contrib.sites.shortcuts import get_current_site
from rest_framework import request
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from src.users.utils import Util


class ProfileService:
    @classmethod
    def add_to_favorite(cls, user, tour):
        user.favorite_tour.add(tour)

    @classmethod
    def remove_from_favorite(cls, user, tour):
        user.favorite_tour.remove(tour)

    @classmethod
    def get_favorite_tour(cls, instance):
        data = instance.favorite_tour.values("id", "title", "slug")
        return data

    @classmethod
    def send_email(cls, user, email):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        email_body = (
            "Hi "
            + user.username.title()
            + "! "
            + " Use link below to verify your  email\n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data)
