from flask import Flask, render_template, request
from models import Product
from forms import ProductForm

app = Flask(__name__)
app.config["SECRET_KEY"] = '123456789'

product1 = Product('Milk', 100, 'l', 2.3)
product2 = Product('Coffee', 300, 'kg', 5)
product3 = Product('Potato', 1000, 'kg', 1.5)
product4 = Product('Sugar', 500, 'kg', 6)
list_of_products = {}

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/list_of_products', methods = ["GET", "POST"])
def products_list():
    form = ProductForm()
    if request.method == "POST":
        product_name = form.product_name.data
        product_quantity = form.product_quantity.data
        product_unit = form.product_unit.data
        product_unit_price = form.product_unit_price.data
        product = Product(product_name, product_quantity, product_unit, product_unit_price)
        if product_name in list_of_products.keys():
            existing_product = Product(product_name, list_of_products[product_name][0], list_of_products[product_name][1], list_of_products[product_name][2])
            existing_product.quantity += product_quantity
            existing_product.unit_price = product_unit_price
            list_of_products[product_name] = [existing_product.quantity, existing_product.unit, existing_product.unit_price]
        else:
            list_of_products[product.name] = [product.quantity, product.unit, product.unit_price]
        return render_template('list_of_products.html', list_of_products=list_of_products, form=form)
    else:
        return render_template('list_of_products.html', list_of_products=list_of_products, form=form)

if __name__ == '__main__':
    app.run(debug = True)
