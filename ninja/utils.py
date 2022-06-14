import inspect
import os
from typing import TYPE_CHECKING, Callable, Optional, cast

from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden
from django.middleware.csrf import CsrfViewMiddleware
from django.template.backends.django import DjangoTemplates

from ninja.types import DictStrAny

__all__ = ["check_csrf", "is_debug_server", "normalize_path"]

if TYPE_CHECKING:
    # Template is missing from django-stubs.
    from django.template.backends.django import Template as DT  # type: ignore


def replace_path_param_notation(path: str) -> str:
    return path.replace("{", "<").replace("}", ">")


def normalize_path(path: str) -> str:
    while "//" in path:
        path = path.replace("//", "/")
    return path


def check_csrf(
    request: HttpRequest, callback: Callable
) -> Optional[HttpResponseForbidden]:
    mware = CsrfViewMiddleware(lambda x: HttpResponseForbidden())  # pragma: no cover
    request.csrf_processing_done = False  # type: ignore
    mware.process_request(request)
    return mware.process_view(request, callback, (), {})


def is_debug_server() -> bool:
    """Check if running under the Django Debug Server"""
    return settings.DEBUG and any(
        s.filename.endswith("runserver.py") and s.function == "run"
        for s in inspect.stack()[1:]
    )


class LocalDjangoTemplates(DjangoTemplates):
    """
    A Django templates backend that can find templates within this application
    even if it isn't installed.
    """

    def __init__(self, params: Optional[DictStrAny] = None):
        local_params = {
            "NAME": "local_templates",
            "DIRS": [],
            "APP_DIRS": False,
        }
        if params:
            local_params.update(params)
        super().__init__(local_params)
        # Explicitly add this app's templates to the template dirs.
        self.dirs.append(os.path.join(os.path.dirname(__file__), "templates"))

    def get_template(self, template_name: str) -> "DT":
        tpl = super().get_template(template_name)
        # django-stubs is misreporting the return type of get_template, so cast
        # it explicitly.
        return cast("DT", tpl)


local_templates_engine = LocalDjangoTemplates()
