from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin


User = get_user_model()


def check_in_group(user, group_name: str) -> bool:
    """Check if the user is in the group, wrapper for the `is_in_group` function."""
    return is_in_group(user, group_name)


def is_in_group(user, group_name: str) -> bool:
    """Check if the user is in the group."""
    try:
        return (
            Group.objects.get(name=group_name).user_set.filter(pk=user.pk).exists()
        )
    except Group.DoesNotExist:
        return False


class HasGroupPermission:
    """
    Allows access only to users in the specified groups.

    The groups should be specified in the view's `permission_groups` attribute
    in the following format:
    ```
    {
        "action": ["group1", "group2", ...],
        ...
    }
    ```

    .. note::
        Thanks [inoyatov](https://gist.github.com/inoyatov/d4bca6d07bd57fdfe6bbc3872a4b8b7f) for the github gist

    .. attention::
        This permission class assumes the user is authenticated.
    """

    permission_groups = {}  # By default, no access

    @classmethod
    def has_permission(cls, request, view):
        return cls.has_action_permission(request, view, view.action)

    @staticmethod
    def has_action_permission(request, view, action):
        required_groups = view.permission_groups.get(action)
        if required_groups == None:
            # If the action is not specified, always deny access
            return False
        elif "_Public" in required_groups:
            # If the action is public, always allow access
            return True
        else:
            # Check if the user is in the required action group
            return any(
                check_in_group(request.user, group_name)
                for group_name in required_groups
            )


class IsAuthenticated:
    """
    Allows access only to authenticated and active users.
    """

    def _has_permission(self, request):
        return request.user and request.user.is_authenticated and request.user.is_active

    def has_permission(self, request, view):
        return self._has_permission(request)

    def has_object_permission(self, request, view, obj):
        return self._has_permission(request)


class IsAdminUser:
    """
    Allows access only to active admin users (staff).
    """

    def _has_permission(self, request):
        return request.user and request.user.is_staff and request.user.is_active

    def has_permission(self, request, view):
        return self._has_permission(request)

    def has_object_permission(self, request, view, obj):
        return self._has_permission(request)


def in_admin_group(user):
    return is_in_group(user, "admins")


class InAdminGroup:
    """Check if the user is in the admin group."""

    def has_permission(self, request, view):
        return in_admin_group(request.user)

    def has_object_permission(self, request, view, obj):
        return in_admin_group(request.user)


def is_superuser(user):
    return user and user.is_superuser


class IsSuperUser:
    """Allows access only to superusers."""

    def has_permission(self, request, view):
        return is_superuser(request.user)

    def has_object_permission(self, request, view, obj):
        return is_superuser(request.user)


def in_superuser_group(user):
    return is_in_group(user, "superusers")


class InSuperserGroup:
    """Check if the user is in the superuser group."""

    def has_permission(self, request, view):
        return in_superuser_group(request.user)

    def has_object_permission(self, request, view, obj):
        return in_superuser_group(request.user)
