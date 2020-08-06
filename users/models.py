import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from config import settings
from core import managers as core_managers


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = ((LANGUAGE_ENGLISH, "en"), (LANGUAGE_KOREAN, "kr"))

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(blank=True, upload_to="avatar")
    avatar_thumbnail = ImageSpecField(
        source="avatar",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=False)
    login_method = models.CharField(
        max_length=6, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )
    objects = core_managers.CustomUserManager()

    def verify_email(self):
        secret = uuid.uuid4().hex[:20]
        self.email_secret = secret
        html_message = render_to_string("emails/verify_email.html", {"secret": secret})
        send_mail(
            "Verify Airbnb-clone Account",
            strip_tags(html_message),
            from_email=settings.EMAIL_FROM,
            recipient_list=[self.email],
            fail_silently=False,
            html_message=html_message,
        )
        self.save()

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
