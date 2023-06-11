from rest_framework.permissions import BasePermission

from directorio.models import User

# class es_proveedor(BasePermission):

#     def has_permission(self, request, view):

#         try:
#             Proveedor.objects.get(usuario = request.user)
#         except Proveedor.DoesNotExist:
#             return False
#         return True
