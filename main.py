from flask import Flask, render_template, request, redirect, url_for
from controller.controller_order import ControllerOrder
from controller.controller_product import ControllerProduct

app = Flask(__name__)

controller_order = ControllerOrder()
controller_product = ControllerProduct()

current_order = None

@app.route('/')
def index():
    products = controller_product.get_all_products()
    return render_template('screen_main.html', products=products)

@app.route('/create_order', methods=['POST'])
def create_order():
    global current_order
    client_name = request.form['client_name']
    current_order = controller_order.create_order(client_name)
    return redirect(url_for('order_form'))

@app.route('/order')
def order_form():
    if not current_order:
        return redirect(url_for('index'))
    return render_template('form_order.html', order=current_order)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    for product in controller_product.get_all_products():
        if product.name == product_name:
            current_order.add_product(product)
            break
    return redirect(url_for('order_form'))

@app.route('/remove_product', methods=['POST'])
def remove_product():
    product_name = request.form['product_name']
    current_order.remove_product(product_name)
    return redirect(url_for('order_form'))

@app.route('/confirm_order')
def confirm_order():
    qr_path = controller_order.generate_qr(current_order.id)
    return render_template('form_order.html', order=current_order, qr_path=qr_path, confirmed=True)

if __name__ == '__main__':
    app.run(debug=True)
