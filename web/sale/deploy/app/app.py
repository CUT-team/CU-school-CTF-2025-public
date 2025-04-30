from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

products = [
    {"id": 1, "name": "Книга по Python", "price": 50, "image": "https://simg.marwin.kz/media/catalog/product/cache/8d1771fdd19ec2393e47701ba45e606d/1/0/10547275_0.jpg"},
    {"id": 2, "name": "Наклейки с логотипом", "price": 10, "image": "https://img.joomcdn.net/7062554b62aecba7bbd00a7f01d0f0010a256e1e_original.jpeg"},
    {"id": 3, "name": "Кружка хакера", "price": 25, "image": "https://cdn1.ozone.ru/s3/multimedia-k/6142479128.jpg"},
    {"id": 4, "name": "Флаг", "price": 1000, "image": "https://cdn.culture.ru/images/65d6908f-a563-53c1-aa17-d29cfaeb510e"},
]

INITIAL_BALANCE = 799


@app.before_request
def initialize_session():
    if 'balance' not in session:
        session['balance'] = INITIAL_BALANCE
    if 'cart' not in session:
        session['cart'] = []
    if 'applied_promo' not in session:
        session['applied_promo'] = None


@app.route('/')
def index():
    return render_template('index.html', products=products, balance=session['balance'])


@app.route('/profile')
def profile():
    return render_template('profile.html', balance=session['balance'])


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)

    if product:
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
        flash(f"{product['name']} добавлен в корзину!", "success")
    else:
        flash("Товар не найден", "danger")

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])

    subtotal = sum(item['price'] for item in cart_items)
    discount = 0

    if session.get('applied_promo'):
        promo = session.get('applied_promo')
        discount_percent = int(promo.replace('SALE', ''))
        discount = subtotal * discount_percent / 100

    total = subtotal - discount

    return render_template(
        'cart.html',
        cart_items=cart_items,
        subtotal=subtotal,
        discount=discount,
        total=total,
        applied_promo=session.get('applied_promo')
    )


@app.route('/apply_promo', methods=['POST'])
def apply_promo():
    promo_code = request.form.get('promo_code', '').upper().strip()

    if re.match(r'^SALE\d+$', promo_code):
        session['applied_promo'] = promo_code
        flash(f"Промокод {promo_code} применен!", "success")
    else:
        flash("Недействительный промокод", "danger")

    return redirect(url_for('cart'))


@app.route('/clear_promo', methods=['POST'])
def clear_promo():
    session['applied_promo'] = None
    flash("Промокод удален", "info")
    return redirect(url_for('cart'))


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session['applied_promo'] = None
    flash("Корзина очищена", "info")
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['POST'])
def checkout():
    cart_items = session.get('cart', [])

    if not cart_items:
        flash("Ваша корзина пуста", "danger")
        return redirect(url_for('cart'))

    subtotal = sum(item['price'] for item in cart_items)
    discount = 0

    if session.get('applied_promo'):
        promo = session.get('applied_promo')
        discount_percent = int(promo.replace('SALE', ''))
        discount = subtotal * discount_percent / 100

    total = subtotal - discount

    if session['balance'] < total:
        flash("Недостаточно средств для покупки", "danger")
        return redirect(url_for('cart'))

    session['balance'] -= total

    flag_item = next((item for item in cart_items if item['name'] == 'Флаг'), None)

    if flag_item:
        flash("cuctf{w0w_1_am_r1ch}", "success")
    else:
        flash("Спасибо за покупку!", "success")

    session['cart'] = []
    session['applied_promo'] = None

    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    flash("Все данные сброшены", "info")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)