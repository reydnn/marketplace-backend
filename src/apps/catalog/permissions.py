from rest_framework.permissions import SAFE_METHODS, BasePermission


class CategoryPermissions(BasePermission):
    """Класс пермишенов с CRUD операциями модели Category"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class ProductsPermissions(CategoryPermissions):
    """Класс пермишенов с CRUD операциями модели Products"""
