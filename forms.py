from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, HiddenField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    product_name = StringField('Name', validators = [DataRequired()])
    product_quantity = IntegerField('Quantity', validators = [DataRequired()])
    product_unit = StringField('Unit', validators = [DataRequired()])
    product_unit_price = DecimalField('Unit Price', validators = [DataRequired()])

class SellProductForm(FlaskForm):
    sell_quantity = IntegerField('Quantity', validators = [DataRequired()])
    product_name = HiddenField()
