"""
Views to create, read, update, and delete model instances.
"""

import sqlalchemy.orm


class ModelViewMixin:
    """
    A mixin for views that process an SQLAlchemy model class.
    """

    # The SQLAlchemy database session.
    # TODO: Consider setting `flask.g.database_session` to the scoped session.
    database_session: sqlalchemy.orm.scoped_session

    # The model class.
    model: type


class ModelInstanceViewMixin(ModelViewMixin):
    """
    A mixin for views that process model instances.
    """

    # The model instances for the current request.
    request_model_instances = []

    def get_model_instances(self) -> list:
        """
        Get the model instances.
        """

        raise NotImplementedError


class OneModelInstanceViewMixin(ModelViewMixin):
    """
    A mixin for views that process one model instance.
    """

    # The model instance for the current request.
    request_model_instance = None

    def get_model_instance(self):
        """
        Get the model instance.
        """

        raise NotImplementedError
