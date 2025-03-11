from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from pyserver_tools.permissions import is_in_group, HasGroupPermission
from django.http import HttpRequest


class TestHasGroupPermission(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345", email="test@example.com"
        )
        self.group = Group.objects.create(name="testgroup")
        self.other_group = Group.objects.create(name="othergroup")
        self.dummy_permission = Permission.objects.create(
            name="Dummy Permission",
            codename="dummy_permission",
            content_type_id=1,
        )
        self.group.permissions.add(self.dummy_permission)
        self.user.groups.add(self.group)

    def test_is_in_group(self):
        self.assertTrue(is_in_group(self.user, "testgroup"))
        self.assertFalse(is_in_group(self.user, "nonexistentgroup"))

    def test_has_group_permission(self):
        # Create a dummy view with a permission group
        # and a request with the user
        class DummyView:
            permission_groups = {"get": ["testgroup"]}
            action = None

        view = DummyView()
        dummy_request = HttpRequest()
        dummy_request.user = self.user
        dummy_request.method = "GET"

        # Should be false as we have not set a view action
        self.assertFalse(HasGroupPermission().has_permission(dummy_request, view))

        # Should be True as the user is in the group
        view.action = "get"
        self.assertTrue(HasGroupPermission().has_permission(dummy_request, view))

        # Should be False as the user is not in the group
        view.permission_groups = {"get": ["nonexistentgroup"]}
        self.assertFalse(HasGroupPermission().has_permission(dummy_request, view))

        # Should be False as the user is not in the group
        view.permission_groups = {"get": ["othergroup"]}
        self.assertFalse(HasGroupPermission().has_permission(dummy_request, view))

        # Should be True as the user is not in the group but the _Public group is allowed
        view.permission_groups = {"get": ["_Public"], "post": ["testgroup"]}
        self.assertTrue(HasGroupPermission().has_permission(dummy_request, view))

        # Should be True as the method is post and the user is in the group
        view.action = "post"
        self.assertTrue(HasGroupPermission().has_permission(dummy_request, view))

        # Should be False as the method is post and the user is not in the group
        view.permission_groups = {"get": ["testgroup"], "post": ["nonexistentgroup"]}
        self.assertFalse(HasGroupPermission().has_permission(dummy_request, view))
