from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from .permissions import check_in_group, HasGroupPermission


class HasGroupPermissionMixin(PermissionRequiredMixin):
    """
    Mixin class to check if the user is in the specified groups.

    Alias for `HasGroupPermission`.
    """

    def has_permission(self):
        return HasGroupPermission.has_action_permission(self.request, self, self.request.method)
