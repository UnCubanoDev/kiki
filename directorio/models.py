from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse

Order = None

def get_order_model():
    global Order
    if Order is None:
        from api.models import Order
    return Order

phone_validator = RegexValidator(
    r'^\+[1-9]\d{1,14}$', _('phone number in the format '))

class User(AbstractUser):
    phone = models.CharField(
        _("phone number"), 
        max_length=18, 
        validators=[phone_validator],
        unique=True
    )
    image = models.ImageField(
        _("imagen"), upload_to='usuarios/', null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)

    class Meta:
        app_label = 'directorio'

class Address(models.Model):
    name = models.CharField(_("name"), max_length=240)
    details = models.CharField(_("details"), max_length=240)
    long = models.CharField(_("longitude"), max_length=50)
    lat = models.CharField(_("latitude"), max_length=50)
    receiver_name = models.CharField(
        _("reciever name"), max_length=80, blank=True, null=True)
    phone = models.CharField(
        _("phone number"), max_length=18, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_(
        "user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("address_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, 
        verbose_name=_("address"), 
        on_delete=models.CASCADE,
        related_name='directorio_orders'
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled'))
        ],
        default='pending'
    )

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
