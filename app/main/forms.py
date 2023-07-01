from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, \
     SelectField
from wtforms.validators import ValidationError, DataRequired, Length, Email, \
     NumberRange
from app.models import User, Location, Product, Category, Role

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role')
    submit = SubmitField('Submit')
    
    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
    
class EditLocationForm(FlaskForm):
    editname = StringField('Location Name', validators=[DataRequired()])
    editsubmit = SubmitField('Save Changes')

class AddLocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class EditCategoryForm(FlaskForm):
    editname = StringField('Category Name', validators=[DataRequired()])
    editsubmit = SubmitField('Save Changes')
            
class AddCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    qty = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    category = SelectField('Category')
    submit = SubmitField('Save Changes')

class EditProductForm(FlaskForm):
    editname = StringField('Product Name', validators=[DataRequired()])
    editqty = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    editcategory = SelectField('Category')
    editsubmit = SubmitField('Save Changes')
    
class TransferProductForm(FlaskForm):
    product = SelectField('Product Name')
    floc = SelectField('Source')
    tloc = SelectField('Destination')
    qty = IntegerField('Quantity', validators=[NumberRange(min=1, max=1000000),DataRequired()])
    submit = SubmitField('Move')