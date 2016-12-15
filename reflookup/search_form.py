from flask_wtf import FlaskForm as Form
from wtforms import TextAreaField, BooleanField
from wtforms.validators import DataRequired


class ReferenceLookupForm(Form):
    """
    This class its a simple view, for show the behavior of our API. It was used for show how the crsearch endpoint works.
    """
    query = TextAreaField(u'Query:', validators=[DataRequired()])
    chkbox = BooleanField(u'Get list of results:')
