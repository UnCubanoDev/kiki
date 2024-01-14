from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from django.core import mail
from django.dispatch import receiver
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from directorio.helper import send_whatsapp_message

phone_validator = RegexValidator(
    r'^\+[1-9]\d{1,14}$', _('phone number in the format '))

# Create your models here.


class Address(models.Model):

    name = models.CharField(_("name"), max_length=240)
    details = models.CharField(_("details"), max_length=240)
    long = models.CharField(_("longitude"), max_length=50)
    lat = models.CharField(_("latitude"), max_length=50)
    receiver_name = models.CharField(
        _("reciever name"), max_length=80, blank=True, null=True)
    phone = models.CharField(
        _("phone number"), max_length=18, blank=True, null=True)
    user = models.ForeignKey("directorio.User", verbose_name=_(
        "user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("address_detail", kwargs={"pk": self.pk})


class User(AbstractUser):

    phone = models.CharField(
        max_length=25,
        validators=[phone_validator], unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    image = models.ImageField(
        _("imagen"), upload_to='usuarios/', null=True, blank=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    is_active = models.BooleanField(_("active"), default=False)

    def __str__(self) -> str:
        return self.first_name or self.phone


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    context = {
        'phone': reset_password_token.user.phone[1:],
        'message': f'This is your key\n{reset_password_token.key}'
    }
    send_whatsapp_message(context["message"], context["phone"])
