from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Restaurant, Distributor, Product


class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsProvider(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(Restaurant.objects.first(user=user))


class IsProductOwner(BasePermission):

    def has_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        restaurant = Restaurant.objects.first(user=request.user)

        if not restaurant:
            return False

        return obj.restaurant == restaurant


class IsDistributor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(Distributor.objects.first(user=user))
