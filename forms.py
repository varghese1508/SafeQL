from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class centralForm(FlaskForm):
    # cmpname -> Company Name
    cmpName = StringField('Company Name', validators=[DataRequired(), 
                                                    Length(min=2, max=50)])
    submit = SubmitField ('Search') # param is just the display label

class addCompanyForm(FlaskForm):
    # cmpName -> Company Name
    cmpName = StringField('Company Name', validators=[DataRequired(), 
                                                    Length(min=2, max=50)])
    phoneNo = StringField('Phone Number', validators=[DataRequired(), 
                                                    Length(min=1, max=15)])
    address = StringField('Address', validators=[DataRequired(), 
                                                    Length(min=1, max=100)])
    submit = SubmitField ('Add') # param is just the display label