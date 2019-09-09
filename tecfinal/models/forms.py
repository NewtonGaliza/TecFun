from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])

    def insert_data(self, item):
        self.name.data = item.name