from flask import Flask, render_template, request, redirect, url_for, flash
from models import Product
from forms import ProductForm, SellProductForm
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = '123456789'

list_of_products = {}
sold_products = {}

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/list_of_products', methods = ["GET", "POST"])
def products_list():
    form = ProductForm()
    if request.method == "POST":
        product_name = form.product_name.data
        product_quantity = form.product_quantity.data
        product_quantity = int(product_quantity)
        product_unit = form.product_unit.data
        product_unit_price = form.product_unit_price.data
        product_unit_price = float(product_unit_price)
        product = Product(product_name, product_quantity, product_unit, product_unit_price)
        if product_name in list_of_products.keys():
            existing_product = Product(product_name, list_of_products[product_name][0], list_of_products[product_name][1], list_of_products[product_name][2])
            existing_product.quantity += product_quantity
            existing_product.unit_price = float(product_unit_price)
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
            new_quantity = int(list_of_products[product_name][0]) - int(sell_quantity)
            list_of_products[product_name][0] = int(new_quantity)
        elif product_name not in list_of_products.keys():
            flash("We do not have such a product.")
            return render_template('sell.html', product_name = product_name, form = form, list_of_products = list_of_products)
        if product_name not in sold_products.keys():
               sold_products[product_name] = [sell_quantity, list_of_products[product_name][1], list_of_products[product_name][2]]
        else:
            sold_products[product_name] = [int(sold_products[product_name][0]) + int(sell_quantity), sold_products[product_name][1], sold_products[product_name][2]]
        return redirect(url_for('products_list'))
    return render_template('sell.html', product_name = product_name, form = form, list_of_products = list_of_products)
@app.route('/cost')
def get_cost():
    cost = [float(value[0]) * float(value[2]) for key, value in list_of_products.items()]
    cost = sum(cost)
    return render_template('cost.html', cost = cost, list_of_products = list_of_products)

@app.route('/income')
def get_income():
    income = [float(value[0]) * float(value[2]) for key, value in sold_products.items()]
    income = sum(income)
    return render_template('income.html', income = income, sold_products = sold_products)

@app.route('/revenue')
def get_revenue():
    cost = [float(value[0]) * float(value[2]) for key, value in list_of_products.items()]
    income = [float(value[0]) * float(value[2]) for key, value in sold_products.items()]
    cost = sum(cost)
    income = sum(income)
    revenue = income - cost
    return render_template('revenue.html', revenue = revenue)

@app.route('/save')
def save_products():
    filename = "products.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product', 'Quantity', 'Unit', 'Unit Price'])
        for key, value in list_of_products.items():
            row = [key] + value
            writer.writerow(row)

    filename_1 = "sold_products.csv"
    with open(filename_1, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product', 'Quantity', 'Unit', 'Unit Price'])
        for key, value in sold_products.items():
            row = [key] + value
            writer.writerow(row)
    return redirect('/')

@app.route('/load')
def load():
    list_of_products.clear()
    with open("products.csv", newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            key = row[0]
            value1, value2, value3 = row[1:]
            list_of_products[key] = [float(value1), value2, float(value3)]

    sold_products.clear()
    with open("sold_products.csv", newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            key = row[0]
            value1, value2, value3 = row[1:]
            sold_products[key] = [float(value1), value2, float(value3)]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)
