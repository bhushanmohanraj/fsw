"""
A view to render a template with context.
"""

import flask
import flask.views


class TemplateMixin:
    """
    A mixin for views that render a template with context.
    """

    # The Flask template name to render.
    template_name: str = ""

    # The context dictionary with which to render the template.
    template_context: dict = {}

    def get_template_name(self) -> str:
        """
        Get the Flask template name to render.
        """

        return self.template_name

    def _get_template_name(self) -> str:
        """
        Internally get the Flask template name to render.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.

        If this method returns `None`, the view returns an HTTP 404 error.
        """

        return self.get_template_name()

    def get_template_context(self) -> dict:
        """
        Get the context dictionary to render the template.
        """

        return self.template_context

    def _get_template_context(self) -> dict:
        """
        Internally get the context dictionary to render the template.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        return self.get_template_context()


class TemplateView(flask.views.View, TemplateMixin):
    """
    A view that renders a template with context.
    """

    def dispatch_request(self, **kwargs):
        """
        Render the template with the template context.
        """

        template_name = self._get_template_name()

        if not template_name:
            return flask.abort(404)

        return flask.render_template(
            template_name,
            **self._get_template_context(),
        )
