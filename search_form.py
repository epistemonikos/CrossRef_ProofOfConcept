from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class CrossRefForm(Form):
    query = StringField('Query', validators=[DataRequired()])
