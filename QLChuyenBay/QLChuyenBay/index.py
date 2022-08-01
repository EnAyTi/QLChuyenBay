import hashlib
import cloudinary.uploader
from QLChuyenBay.admin import *
from QLChuyenBay import app, login
from QLChuyenBay.models import UserRole, User
from flask_login import login_user, login_required
from flask import render_template, request, redirect, url_for, session, jsonify


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.context_processor
def common_attribute():
    return {
        'san_bays': utils.load_san_bay(),
        'cart_stats': utils.cart_stats(session.get('cart')),
        'tuyen_bays': utils.load_tuyen_bay()
    }


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get('avatar')
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res['secure_url']
            try:
                utils.add_user(name=name, password=password, username=username, email=email, avatar=avatar)
                return redirect(url_for('signin'))
            except Exception as ex:
                err_msg = 'Đã có lỗi xảy ra: ' + str(ex)
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = 'Tên người dùng hoặc mật khẩu không chính xác'

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def admin_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        user = User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()
        if user and (user.user_role == UserRole.ADMIN or user.user_role == UserRole.EMPLOYEE):
            login_user(user=user)
        else:
            err_msg = 'Tên người dùng hoặc mật khẩu không chính xác'

    return redirect('/admin')


@app.route('/user-logout')
def signout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/result')
def result():
    err_msg = ''

    san_bay_di_id = request.args.get('diemdi')
    san_bay_den_id = request.args.get('diemden')
    khoihanh = request.args.get('khoihanh')

    tuyenbay = utils.check_tuyen_bay(san_bay_di_id=san_bay_di_id, san_bay_den_id=san_bay_den_id)
    if tuyenbay:
        chuyen_bay = utils.check_chuyen_bay(tuyenbay.id)
        if chuyen_bay:
            chuyen_bays = utils.load_chuyen_bay(tuyenbay.id, khoihanh)
            return render_template('flight.html', chuyen_bays=chuyen_bays)
        else:
            err_msg = 'Không có chuyến bay nào'
    else:
        err_msg = 'Không có chuyến bay nào'
    return render_template('flight.html', err_msg=err_msg)


@app.route("/chuyen-bay/<int:chuyenbay_id>")
def chuyen_bay(chuyenbay_id):
    chuyenbay = utils.get_chuyen_bay_by_id(chuyenbay_id=chuyenbay_id)
    tuyenbay = utils.get_tuyen_bay_by_id(chuyenbay.ma_tuyen_bay)
    sanbaydi = utils.get_san_bay_by_id(tuyenbay.ma_san_bay_di)
    sanbayden = utils.get_san_bay_by_id(tuyenbay.ma_san_bay_den)
    ve = utils.load_ve(chuyenbay_id=chuyenbay.id)
    return render_template('chuyen-bay.html', chuyenbay=chuyenbay,
                           tuyenbay=tuyenbay, sanbaydi=sanbaydi, sanbayden=sanbayden, ve=ve)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/add-to-cart', methods=['post'])
def add_to_cart():
    data = request.json
    mave = str(data.get('mave'))
    machuyenbay = str(data.get('machuyenbay'))
    gia = data.get('gia')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if mave in cart:
        cart[mave]['quantity'] = cart[mave]['quantity'] + 1
    else:
        cart[mave] = {
            'mave': mave,
            'machuyenbay': machuyenbay,
            'gia': gia,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<mave_id>', methods=['delete'])
def delete_cart(mave_id):
    cart = session.get('cart')
    if cart:
        if mave_id in cart:
            del cart[mave_id]
            session['cart'] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_hoadon(session.get('cart'))

        del session['cart']
        return jsonify({'code': 200})
    except Exception as ex:
        print(str(ex))
        return jsonify({'code': 400})


if __name__ == "__main__":
    app.run(debug=True)
