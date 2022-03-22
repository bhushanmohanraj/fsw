from sqlalchemy.orm import declared_attr


class ClassNameModelMixin:
    """
    Set the table name to the model class name.
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__
