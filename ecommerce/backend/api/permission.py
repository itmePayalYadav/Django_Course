from rest_framework import permissions

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False
        return super().has_permission(request, view)

    def has_permission(self, request, view):
        print(request.user.get_all_permissions())
        if request.user.is_staff:
            if request.user.has_perm("products.add_product"):
                return True
            if request.user.has_perm("products.delete_product"):
                return True
            if request.user.has_perm("products.change_product"):
                return True
            if request.user.has_perm("products.view_product"):
                return True
            return False
        return False
 