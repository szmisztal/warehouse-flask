from flask import Flask, render_template, request, redirect, url_for, flash
from models import Product
from forms import ProductForm, SellProductForm
from decimal import Decimal

app = Flask(__name__)
app.config["SECRET_KEY"] = '123456789'

product1 = Product('Milk', 100, 'l', 2.3)
product2 = Product('Coffee', 300, 'kg', 5)
product3 = Product('Potato', 1000, 'kg', 1.5)
product4 = Product('Sugar', 500, 'kg', 6)
list_of_products = {}
sold_products = {}
list_of_products['Milk'] = [100, 'l', 2.3]
list_of_products['Coffee'] = [300, 'kg', 5]
list_of_products['Potato'] = [1000, 'kg', 1.5]
list_of_products['Sugar'] = [500, 'kg', 6]
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/list_of_products', methods = ["GET", "POST"])
def products_list():
    form = ProductForm()
    if request.method == "POST":
        product_name = form.product_name.data
        product_quantity = form.product_quantity.data
        product_quantity = float(product_quantity)
        product_unit = form.product_unit.data
        product_unit_price = form.product_unit_price.data
        product_unit_price = float(product_unit_price)
        product = Product(product_name, product_quantity, product_unit, product_unit_price)
        if product_name in list_of_products.keys():
            existing_product = Product(product_name, list_of_products[product_name][0], list_of_products[product_name][1], list_of_products[product_name][2])
            existing_product.quantity += product_quantity
            existing_product.unit_price = product_unit_price
            list_of_products[product_name] = [existing_product.quantity, existing_product.unit, existing_product.unit_price]
        else:
            list_of_products[product.name] = [product.quantity, product.unit, product.unit_price]
        return render_template('list_of_products.html', list_of_products = list_of_products, form = form)
    else:
        return render_template('list_of_products.html', list_of_products = list_of_products, form = form)

@app.route('/list_of_sold_products')
def list_of_sold_products():
    return render_template('sold_products.html', sold_products = sold_products)

@app.route('/sell/<product_name>', methods = ["GET", "POST"])
def sell_product(product_name):
    form = SellProductForm()
    if request.method == "POST" and form.validate_on_submit():
        sell_quantity = form.sell_quantity.data
        if product_name in list_of_products.keys():
            new_quantity = float(list_of_products[product_name][0]) - float(sell_quantity)
            list_of_products[product_name][0] = float(new_quantity)
        elif product_name not in list_of_products.keys():
            flash("We do not have such a product.")
            return render_template('sell.html', product_name = product_name, form = form, list_of_products = list_of_products)
        if product_name not in sold_products.keys():
               sold_products[product_name] = [sell_quantity, list_of_products[product_name][1], list_of_products[product_name][2]]
        else:
            sold_products[product_name] = [float(sold_products[product_name][0]) + float(sell_quantity), sold_products[product_name][1], sold_products[product_name][2]]
        return redirect(url_for('products_list'))
    return render_template('sell.html', product_name = product_name, form = form, list_of_products = list_of_products)
@app.route('/cost')
def get_cost():
    cost = 0
    for key, value in list_of_products.items():
        i = value[0] * value[2]
        cost += i
        cost = round(cost, 2)
    return cost and render_template('cost.html', cost = cost, list_of_products = list_of_products)

@app.route('/income')
def get_income():
    income = 0
    for key, value in sold_products.items():
        i = value[0] * value[2]
        income +=i
        income = round(income, 2)
    return income and render_template('income.html', income = income, sold_products = sold_products)

if __name__ == '__main__':
    app.run(debug = True)
