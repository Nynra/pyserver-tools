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


logger = logging.getLogger(__name__)


def error_page(request):
    error_message = "An error occurred. Please try again later."
    previous_page_url = request.META.get("HTTP_REFERER", "/")
    context = {"error_message": error_message, "previous_page_url": previous_page_url}
    logger.error(
        f"An error occurred. User {request.user} tried to access a page that does not exist. Page {request.path}"
    )
    return render(request, "error_page.html", context)


class BaseCreateView(CreateView):
    """Base view for creating a new model instance.

    This is a base class for creating a new model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - detail_view_name: The name of the detail view.
    - list_view_name: The name of the list view.
    """

    template_name = "create_model.html"
    context_object_name = "item"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "detail_view_name"):
            raise AttributeError("detail_view_name must be set in the subclass")
        if not hasattr(self, "list_view_name"):
            raise AttributeError("list_view_name must be set in the subclass")

    def get_success_url(self) -> str:
        return reverse_lazy(self.detail_view_name, args=[self.object.pk])

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        return context


class BaseUpdateView(UpdateView):
    """Base view for updating an existing model instance.

    This is a base class for updating an existing model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - detail_view_name: The name of the detail view.
    - list_view_name: The name of the list view.
    """

    template_name = "update_model.html"
    context_object_name = "item"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "detail_view_name"):
            raise AttributeError("detail_view_name must be set in the subclass")
        if not hasattr(self, "list_view_name"):
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
        return context


class BaseDeleteView(DeleteView):
    """Base view for deleting an existing model instance.

    This is a base class for deleting an existing model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - list_view_name: The name of the list view.
    """

    template_name = "delete_model.html"
    context_object_name = "item"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "list_view_name"):
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
        return context


class BaseDetailView(DetailView):
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

    template_name = "detail_model.html"
    context_object_name = "item"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "detail_form"):
            raise AttributeError("detail_form must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "list_view_name"):
            raise AttributeError("list_view_name must be set in the subclass")
        if not hasattr(self, "delete_view_name"):
            raise AttributeError("delete_view_name must be set in the subclass")
        if not hasattr(self, "update_view_name"):
            raise AttributeError("update_view_name must be set in the subclass")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.detail_form(
            instance=self.object
        )  # Add the form to the context
        context["model_name"] = self.model_name
        context["list_url"] = self.list_view_name
        context["delete_url"] = self.delete_view_name
        context["update_url"] = self.update_view_name
        return context


class BaseRandomView(View):
    """Base view for showing a random model instance.

    This is a base class for showing a random model instance, it should be subclassed
    and not used directly. The subclass should set the following attributes:

    - template_name: The name of the template to render.
    - model_name: The name of the model.
    - random_view_name: The name of the random view.
    """

    template_name = "random_model.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "random_view_name"):
            raise AttributeError("random_view_name must be set in the subclass")

    def get(self, request, *args, **kwargs):
        model = self.model.get_random(user=self.request.user)
        if model is None:
            # Return no content available
            return render(request, "no_content.html")

        model.update_activation_date()
        form = self.form_class(instance=model)
        logger.info("User {} got a random {}".format(request.user, str(model)))
        return render(request, self.template_name, self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except AttributeError:
            context = {}
        context["form"] = kwargs["form"]
        context["model_name"] = self.model_name
        context["random_item_url"] = self.random_view_name
        return context


class BaseListView(ListView):
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

    template_name = "list_models.html"
    context_object_name = "items"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "template_name"):
            raise AttributeError("template_name must be set in the subclass")
        if not hasattr(self, "model_name"):
            raise AttributeError("model_name must be set in the subclass")
        if not hasattr(self, "update_view_name"):
            raise AttributeError("update_view_name must be set in the subclass")
        if not hasattr(self, "delete_view_name"):
            raise AttributeError("delete_view_name must be set in the subclass")
        if not hasattr(self, "create_view_name"):
            raise AttributeError("create_view_name must be set in the subclass")
        if not hasattr(self, "list_view_name"):
            raise AttributeError("list_view_name must be set in the subclass")

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(
            user_config__user=self.request.user.id
        ).order_by("-id")

    def get(self, request, *args, **kwargs):
        # Get the page number from the request
        page_number = request.GET.get("page")
        queryset = self.get_queryset()  # Get the queryset
        paginator = Paginator(queryset, 10)  # Create a paginator
        page_obj = paginator.get_page(page_number)  # Get the page

        # Return the page
        self.object_list = page_obj.object_list
        context = self.get_context_data()
        context["page_obj"] = page_obj
        return render(request, self.template_name, context)

    # For the template to render correctly the model name variable and list url have to be passed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = self.model_name
        context["update_url"] = self.update_view_name
        context["delete_url"] = self.delete_view_name
        context["create_url"] = self.create_view_name
        context["list_url"] = self.list_view_name
        return context
