from flask_wtf import FlaskForm
from wtforms import TextAreaField


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text')


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

