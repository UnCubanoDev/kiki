from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Restaurant, Distributor


class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsProvider(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return bool(Restaurant.objects.filter(user=user).exists())


class IsProductOwner(BasePermission):

    def has_permission(self, request, obj):

        user = request.user

        if not user.is_authenticated:
            return False

        restaurant = Restaurant.objects.filter(user=user)

        if not restaurant.exists():
            return False

        if request.method in [*SAFE_METHODS, 'POST']:
            return True

        return obj.restaurant == restaurant


class IsDistributor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return bool(Distributor.objects.filter(user=user).exists())


class IsOrderDistributor(BasePermission):

    def has_permission(self, request, obj):
        print(obj)
        # user = request.user
        # if not user.is_authenticated:
        #     return False
        # return bool(Distributor.objects.filter(user=user).exists())


class IsClientAndOrderOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        print(obj)
        user = request.user

        if not user.is_authenticated:
            return False

        return bool(obj.user == user)


class IsOrderPending(BasePermission):

    def has_object_permission(self, request, view, obj):

        print(obj)

        return bool(obj.status == 'pending')
