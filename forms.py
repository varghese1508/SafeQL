from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class centralForm(FlaskForm):
    # cmpname -> Company Name
    cmpname = StringField('CmpName', validators=[DataRequired(), 
                                                    Length(min=2, max=50)])
    submit = SubmitField ('Search') # param is just the display label

class addCompanyForm(FlaskForm):
    # cmpName -> Company Name
    cmpName = StringField('cmpName', validators=[DataRequired(), 
                                                    Length(min=2, max=50)])
    phoneNo = StringField('phoneNo', validators=[DataRequired(), 
                                                    Length(min=1, max=15)])
    address = StringField('address', validators=[DataRequired(), 
                                                    Length(min=1, max=100)])
    submit = SubmitField ('Search') # param is just the display label