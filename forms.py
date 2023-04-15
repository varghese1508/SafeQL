from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class centralForm(FlaskForm):
    # cmpname -> Company Name
    cmpname = StringField('CmpName', validators=[DataRequired(), 
                                                    Length(min=2, max=50)])
    submit = SubmitField ('Search') # param is just the display label