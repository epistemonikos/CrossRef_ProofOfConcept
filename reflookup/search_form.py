from flask_wtf import FlaskForm as Form
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class CrossRefForm(Form):
    query = TextAreaField(u'Query:', validators=[DataRequired()])
