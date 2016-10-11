from flask_wtf import FlaskForm as Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class ReferenceLookupForm(Form):
    query = TextAreaField(u'Query:', validators=[DataRequired()])
