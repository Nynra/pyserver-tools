"""Base Views for Django.

This module contains base views for Django that can be used to create views for
basic database operations using default templates (not in the admin area).

.. attention::

    These views do not implement any autorization or authentication checks. It is
    up to the developer to implement these checks in the views that inherit from
    these base views.
"""

import logging
from typing import Any

# from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.forms import BaseModelForm


logger = logging.getLogger(__name__)


def error_page(request: HttpRequest) -> HttpResponse:
    """Return a custom error page.

    A simple error page that displays an error message and a link to the previous page.
    """
    error_message = "An error occurred. Please try again later."
    previous_page_url = request.META.get("HTTP_REFERER", "/")
    context = {"error_message": error_message, "previous_page_url": previous_page_url}
    logger.error(
        f"An error occurred. User {request.user} tried to access a page that does not exist. Page {request.path}"
    )
    return render(request, "error_page.html", context)


class PyserverBaseCreateView(CreateView):
    """Base view for creating a new model instance.

    This is a base class for creating a new model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - detail_view_name: The name of the detail view.
    - list_view_name: The name of the list view.
    - form_class: The form to use for the create view.

    .. attention::

        The form class is expected to accept the `request_user` as a keyword argument.

    """

    template_name: str = "tools_templates/create_model.html"
    model_name: str = None
    detail_view_name: str = None
    list_view_name: str = None
    form_class: BaseModelForm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.detail_view_name, type(None)):
            raise AttributeError("detail_view_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")
        if isinstance(self.form_class, type(None)):
            raise AttributeError("form_class must be set in the subclass")

    def get_success_url(self) -> str:
        """Return the URL to redirect to after a successful form submission.

        Generate the success url using the `detail_view_name` and the primary key of the object.
        """
        return reverse_lazy(self.detail_view_name, args=[self.object.pk])

    def get_form_kwargs(self):
        """Pass the current user to the form.

        Insert the current user into the form kwargs as `request_user`.
        """
        kwargs = super().get_form_kwargs()
        kwargs["request_user"] = self.request.user  # Pass the user to the form
        return kwargs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add the model name and list url to the context.

        Add the model name and list url to the context so that the template can render correctly.
        """
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class PyserverBaseUpdateView(UpdateView):
    """Base view for updating an existing model instance.

    This is a base class for updating an existing model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - detail_view_name: The name of the detail view.
    - list_view_name: The name of the list view.
    - form_class: The form to use for the update view.

    .. attention::

        The form class is expected to accept the `request_user` as a keyword argument.

    """

    template_name: str = "tools_templates/update_model.html"
    model_name: str = None
    detail_view_name: str = None
    list_view_name: str = None
    form_class: BaseModelForm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.detail_view_name, type(None)):
            raise AttributeError("detail_view_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")
        if isinstance(self.form_class, type(None)):
            raise AttributeError("form_class must be set in the subclass")

    def get_success_url(self) -> str:
        """Return the URL to redirect to after a successful form submission.

        Generate the success url using the `detail_view_name` and the primary key of the object.
        """
        return reverse_lazy(self.detail_view_name, args=[self.object.pk])

    def get_form_kwargs(self) -> dict[str, Any]:
        """Pass the current user to the form.

        Insert the current user into the form kwargs as `request_user`.
        """
        kwargs = super().get_form_kwargs()
        kwargs["request_user"] = self.request.user  # Pass the user to the form
        return kwargs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add the model name and list url to the context.

        Add the model name and list url to the context so that the template can render correctly.
        """
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class PyserverBaseDeleteView(DeleteView):
    """Base view for deleting an existing model instance.

    This is a base class for deleting an existing model instance, it should be subclassed
    and not used directly. This class does not check if the object exists or if the user
    has permission to delete the object.

    The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - list_view_name: The name of the list view.
    - form_class: The form to use for the delete view.

    .. attention::

        The form class is expected to accept the `request_user` as a keyword argument.

    """

    template_name: str = "tools_templates/delete_model.html"
    model_name: str = None
    list_view_name: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")

    def get_success_url(self) -> str:
        """Return the URL to redirect to after a successful form submission.

        Generate the success url using the `list_view_name`.
        """
        return reverse_lazy(self.list_view_name)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add the model name and list url to the context.

        Add the model name and list url to the context so that the template can render correctly.
        """
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class PyserverBaseDetailView(DetailView):
    """Base view for showing an existing model instance.

    This is a base class for showing an existing model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - form_class: The form to use for the detail view.
    - model_name: The name of the model.
    - list_view_name: The name of the list view.
    - delete_view_name: The name of the delete view.
    - update_view_name: The name of the update view.
    """

    template_name: str = "tools_templates/detail_model.html"
    form_class: BaseModelForm = None
    model_name: str = None
    list_view_name: str = None
    delete_view_name: str = None
    update_view_name: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.form_class, type(None)):
            raise AttributeError("form_class must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")
        if isinstance(self.delete_view_name, type(None)):
            raise AttributeError("delete_view_name must be set in the subclass")
        if isinstance(self.update_view_name, type(None)):
            raise AttributeError("update_view_name must be set in the subclass")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Add the model name and list url to the context.

        Add the model name and list url to the context so that the template can render correctly.
        """
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["form"] = self.form_class(instance=self.object)
        context["list_url"] = self.list_view_name
        context["delete_url"] = self.delete_view_name
        context["update_url"] = self.update_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class PyserverBaseListView(ListView):
    """Base view for showing a list of model instances.

    This is a base class for showing a list of model instances, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - update_view_name: The name of the update view.
    - delete_view_name: The name of the delete view.
    - create_view_name: The name of the create view.
    - list_view_name: The name of the list view.
    """

    template_name: str = "tools_templates/list_models.html"
    model_name: str = None
    update_view_name: str = None
    delete_view_name: str = None
    create_view_name: str = None
    list_view_name: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.update_view_name, type(None)):
            raise AttributeError("update_view_name must be set in the subclass")
        if isinstance(self.delete_view_name, type(None)):
            raise AttributeError("delete_view_name must be set in the subclass")
        if isinstance(self.create_view_name, type(None)):
            raise AttributeError("create_view_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        page_obj = self._get_pages(request)
        self.object_list = page_obj.object_list
        context = self.get_context_data()
        context["items"] = page_obj
        return render(request, self.template_name, context)

    def _get_pages(self, request) -> QuerySet:
        """Return the pages object for the queryset."""
        # Get the page number from the request
        page_number = request.GET.get("page")
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 10)
        page_obj = paginator.get_page(page_number)
        return page_obj

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["update_url"] = self.update_view_name
        context["delete_url"] = self.delete_view_name
        context["create_url"] = self.create_view_name
        context["list_url"] = self.list_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context
