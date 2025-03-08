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
    """

    template_name : str = "tools_templates/create_model.html"
    model_name : str = None
    detail_view_name : str = None
    list_view_name : str = None

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

    def get_success_url(self) -> str:
        return reverse_lazy(self.detail_view_name, args=[self.object.pk])

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
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
    """

    template_name : str = "tools_templates/update_model.html"
    context_object_name : str = None
    model_name : str = None
    detail_view_name : str = None
    list_view_name : str = None

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

    def get_success_url(self) -> str:
        logger.info(
            "User {} updated a {}, with id {}".format(
                self.request.user, self.model.__name__, self.object.pk
            )
        )
        return reverse_lazy(self.detail_view_name, args=[self.object.pk])

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        context["previous_page_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class PyserverBaseDeleteView(DeleteView):
    """Base view for deleting an existing model instance.

    This is a base class for deleting an existing model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - list_view_name: The name of the list view.
    """

    template_name : str = "tools_templates/delete_model.html"
    model_name : str = None
    list_view_name : str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")

    def get_success_url(self) -> str:
        logger.info(
            "User {} deleted a {}, with id {}".format(
                self.request.user, self.model.__name__, self.object.pk
            )
        )
        return reverse_lazy(self.list_view_name)

    def form_valid(self, form):
        # Check if the user is also the user in the model object user_config
        if self.object.user_config.user == self.request.user:
            return super().form_valid(form)

        # If the user does not have access return default 403 page
        return super().form_invalid(form)

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
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
    - detail_form: The form to use for the detail view.
    - model_name: The name of the model.
    - list_view_name: The name of the list view.
    - delete_view_name: The name of the delete view.
    - update_view_name: The name of the update view.
    """

    template_name : str = "tools_templates/detail_model.html"
    detail_form : BaseModelForm = None
    model_name : str = None
    list_view_name : str = None
    delete_view_name : str = None
    update_view_name : str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.template_name, type(None)):
            raise AttributeError("template_name must be set in the subclass")
        if isinstance(self.detail_form, type(None)):
            raise AttributeError("detail_form must be set in the subclass")
        if isinstance(self.model_name, type(None)):
            raise AttributeError("model_name must be set in the subclass")
        if isinstance(self.list_view_name, type(None)):
            raise AttributeError("list_view_name must be set in the subclass")
        if isinstance(self.delete_view_name, type(None)):
            raise AttributeError("delete_view_name must be set in the subclass")
        if isinstance(self.update_view_name, type(None)):
            raise AttributeError("update_view_name must be set in the subclass")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.detail_form(
            instance=self.object
        )  # Add the form to the context
        context["item"] = self.object
        context["model_name"] = self.model_name
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

    template_name : str = "tools_templates/list_models.html"
    model_name : str = None
    update_view_name : str = None
    delete_view_name : str = None
    create_view_name : str = None
    list_view_name : str = None

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
        # Return the page
        page_obj = self._get_pages(request)
        self.object_list = page_obj.object_list
        context = self.get_context_data()
        context["items"] = page_obj
        return render(request, self.template_name, context)
    
    def _get_pages(self, request) -> QuerySet:
        """Return the pages for the queryset."""
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
