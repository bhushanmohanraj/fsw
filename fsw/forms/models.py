"""
Convert SQLAlchemy models to WTForms forms.
"""

import typing

import sqlalchemy
import wtforms

_HTML_TIME_FORMAT = "%H:%M"
_HTML_DATE_FORMAT = "%Y-%m-%d"
_HTML_DATETIME_LOCAL_FORMAT = "%Y-%m-%dT%H:%M:%S"


_COLUMN_FIELD_TYPES = {
    sqlalchemy.types.String: wtforms.fields.StringField,
    sqlalchemy.types.Integer: wtforms.fields.IntegerField,
    sqlalchemy.types.DateTime: wtforms.fields.DateTimeLocalField,
    sqlalchemy.types.Date: wtforms.fields.DateField,
    sqlalchemy.types.Time: wtforms.fields.TimeField,
    sqlalchemy.types.Boolean: wtforms.fields.BooleanField,
    sqlalchemy.types.Enum: wtforms.fields.SelectField,
}


def _get_column_field_type(column) -> type:
    """
    Get the WTForms field type corresponding to an SQLAlchemy column.
    """

    try:
        return _COLUMN_FIELD_TYPES[type(column.type)]

    except KeyError:
        raise KeyError(
            f"SQLAlchemy columns of the type `{type(column.type).__name__}`"
            "cannot currently be converted in WTForms fields."
        )


def _get_column_field_kwargs(column) -> dict:
    """
    Get the keyword arguments
    for constructing a WTForms field corresponding to an SQLAlchemy column.
    """
    field_kwargs = {
        "label": column.name.replace("_", " ").title(),
        "description": getattr(column, "doc", None),
        "default": getattr(column, "default", None),
        "validators": [],
    }

    field_kwargs["validators"].append(
        wtforms.validators.Optional() if column.nullable else wtforms.validators.InputRequired()
    )

    if type(column.type) is sqlalchemy.types.String:
        if column.type.length:
            field_kwargs["validators"].append(wtforms.validators.Length(max=column.type.length))

    elif type(column.type) is sqlalchemy.types.DateTime:
        field_kwargs["format"] = _HTML_DATETIME_LOCAL_FORMAT

    elif type(column.type) is sqlalchemy.types.Date:
        field_kwargs["format"] = _HTML_DATE_FORMAT

    elif type(column.type) is sqlalchemy.types.Time:
        field_kwargs["format"] = _HTML_TIME_FORMAT

    elif type(column.type) is sqlalchemy.types.Enum:
        field_kwargs["choices"] = [(choice, choice.title()) for choice in column.type.enums]

    return field_kwargs


class ModelFormMixin:
    """
    Add a class method to create WTForms form classes from SQLAlchemy model classes.
    """

    @classmethod
    def get_model_form(cls, model, field_names: list[str]):
        """
        Create a WTForms form from an SQLAlchemy model.

        The `field_names` parameter should specify the names
        of the columns to convert into form fields.
        """

        class ModelForm(cls):
            """
            The form class created from the model.
            """

        columns = sqlalchemy.inspect(model).c

        for column in columns:
            name = column.name

            if name not in field_names:
                continue

            field_type = _get_column_field_type(column)
            field_kwargs = _get_column_field_kwargs(column)

            setattr(ModelForm, name, field_type(**field_kwargs))

        return ModelForm
