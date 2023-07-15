from django.db import models
from django.db.models import Avg
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

phone_validator = RegexValidator(
    ' ^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$ ', _('phone must be in format'))
min_rating = MinValueValidator(1, 'at least 1')
max_rating = MaxValueValidator(5, 'max 5')


class Restaurant(models.Model):

    name = models.CharField(_("name"), max_length=70)
    description = models.TextField(_("description"))
    address = models.CharField(_("address"), max_length=150)
    phone = models.CharField(_("phone"), max_length=20,)
    image = models.ImageField(
        _("image"), upload_to='restaurants', null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    time = models.CharField(_("time"), max_length=10)
    categories_product = models.ManyToManyField(
        "api.Category", verbose_name=_("Products Categories"))
    is_active = models.BooleanField(_("is active"), default=True)
    tax = models.FloatField(_("tax"), default=10)
    type = models.CharField(_("type"), max_length=50)
    latitude = models.CharField(_("latitude"), max_length=25, default='')
    longitude = models.CharField(_("longitude"), max_length=25, default='')

    @property
    def rating(self):
        return self.restaurantrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def products(self):
        return self.product_set.all()

    def rate(self, user, rating):
        RestaurantRating.objects.update_or_create(
            user=user, restaurant=self, defaults={'rating': int(rating)})

    class Meta:
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("restaurant_detail", kwargs={"pk": self.pk})


class RestaurantRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    restaurant = models.ForeignKey("api.Restaurant", verbose_name=_(
        "restaurant"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("restaurant rating")
        verbose_name_plural = _("restaurant ratings")

    def __str__(self):
        return f'{self.user} -> {self.restaurant}'

    def get_absolute_url(self):
        return reverse("restaurant_rating_detail", kwargs={"pk": self.pk})


class Distributor(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    vehicle_image = models.ImageField(
        _("vehicle image"), upload_to='distributors/vehicles', null=True, blank=True)
    vehicle_id = models.CharField(_("vehicle registration id"), max_length=7)
    vehicle_type = models.CharField(_("vehicle type"), max_length=20)

    @property
    def rating(self):
        return self.distributorrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    def rate(self, user, rating):
        DistributorRating.objects.update_or_create(
            user=user, distributor=self, defaults={'rating': int(rating)})

    class Meta:
        verbose_name = _("distributor")
        verbose_name_plural = _("distributors")

    def __str__(self):
        return self.user.first_name or self.user.email

    def get_absolute_url(self):
        return reverse("distributor_detail", kwargs={"pk": self.pk})


class DistributorRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    distributor = models.ForeignKey("api.Distributor", verbose_name=_(
        "distributor"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("Distributor rating")
        verbose_name_plural = _("Distributor ratings")

    def __str__(self):
        return f'{self.user} -> {self.distributor}'

    def get_absolute_url(self):
        return reverse("distributor_rating_detail", kwargs={"pk": self.pk})


class Category(models.Model):

    name = models.CharField(_("name"), max_length=20)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"))
    price = models.DecimalField(_("price"), max_digits=6, decimal_places=2)
    time = models.CharField(_("time of preparation"), max_length=10)
    image = models.ImageField(
        _("image"), upload_to='products/', null=True, blank=True)
    category = models.ForeignKey("api.Category", verbose_name=_(
        "category"), on_delete=models.PROTECT)
    restaurant = models.ForeignKey("api.Restaurant", verbose_name=_(
        "restaurant"), on_delete=models.CASCADE)
    um = models.CharField(_("unit of measurement"), max_length=10)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def rating(self):
        return self.productrating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    def rate(self, user, rating):
        ProductRating.objects.update_or_create(
            user=user, product=self, defaults={'rating': int(rating)})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class ProductRating(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    product = models.ForeignKey("api.Product", verbose_name=_(
        "product"), on_delete=models.CASCADE)
    rating = models.IntegerField(_("rating"), validators=[
                                 min_rating, max_rating])

    class Meta:
        verbose_name = _("product rating")
        verbose_name_plural = _("product ratings")

    def __str__(self):
        return f'{self.user} -> {self.product}'

    def get_absolute_url(self):
        return reverse("product_rating_detail", kwargs={"pk": self.pk})


class Order(models.Model):

    user = models.ForeignKey(get_user_model(), verbose_name=_(
        "user"), on_delete=models.CASCADE)
    products = models.ManyToManyField(
        "api.Product", verbose_name=_("product"), through='OrderDetail')
    date = models.DateField(_("date"), auto_now=True)
    time = models.TimeField(_("time"), auto_now=True)
    address = models.CharField(_("address"), max_length=200)
    status = models.CharField(_("status"), max_length=15)

    @property
    def total_price(self):
        return sum([product.price for product in self.products.all()])

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})


class OrderDetail(models.Model):

    order = models.ForeignKey("api.Order", verbose_name=_(
        "order"), on_delete=models.CASCADE)
    product = models.ForeignKey("api.Product", verbose_name=_(
        "product"), on_delete=models.CASCADE)
    amount = models.IntegerField(_("amount"), validators=[min_rating])

    class Meta:
        verbose_name = _("order detail")
        verbose_name_plural = _("order details")

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("orderdetail_detail", kwargs={"pk": self.pk})
