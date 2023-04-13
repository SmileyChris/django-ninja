from typing import Any, Dict, Optional

from pydantic.fields import FieldInfo, ModelField

from ninja import params_models

__all__ = ["Param", "Path", "Query", "Header", "Cookie", "Body", "Form", "File"]


class Param(FieldInfo):
    def __init__(
        self,
        default: Any,
        *,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        regex: Optional[str] = None,
        example: Any = None,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        # param_name: Optional[str] = None,
        # param_type: Optional[Any] = None,
        **extra: Any,
    ):
        self.deprecated = deprecated
        # self.param_name: Optional[str] = None
        # self.param_type: Optional[Any] = None
        self.model_field: Optional[ModelField] = None
        if example:
            extra["example"] = example
        if examples:
            extra["examples"] = examples
        if deprecated:
            extra["deprecated"] = deprecated
        if not include_in_schema:
            extra["include_in_schema"] = include_in_schema
        super().__init__(
            default,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            regex=regex,
            **extra,
        )

    @classmethod
    def _param_source(cls) -> str:
        "Openapi param.in value or body type"
        return cls.__name__.lower()


class Path(Param):
    _model = params_models.PathModel


class Query(Param):
    _model = params_models.QueryModel


class Header(Param):
    _model = params_models.HeaderModel


class Cookie(Param):
    _model = params_models.CookieModel


class Body(Param):
    _model = params_models.BodyModel


class Form(Param):
    _model = params_models.FormModel


class File(Param):
    _model = params_models.FileModel


class _MultiPartBody(Param):
    _model = params_models._MultiPartBodyModel
    _param_source = Body._param_source
