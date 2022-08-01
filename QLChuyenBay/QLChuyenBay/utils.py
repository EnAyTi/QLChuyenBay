import hashlib
from sqlalchemy import extract, func
from QLChuyenBay import db
from flask_login import current_user
from datetime import datetime, timedelta
from QLChuyenBay.models import SanBay, TuyenBay, ChuyenBay, User, UserRole, HoaDon, ChiTietHoaDon, Ve, Rule


def load_san_bay():
    return SanBay.query.all()


def load_tuyen_bay():
    return TuyenBay.query.all()


def load_ve(chuyenbay_id):
    if chuyenbay_id:
        return Ve.query.filter(Ve.ma_chuyen_bay.__eq__(chuyenbay_id))

    return Ve.all()


def load_ve2(chuyenbay_id, hangve_id):
    return Ve.query.filter(Ve.ma_chuyen_bay.__eq__(chuyenbay_id), Ve.ma_hang_ve.__eq__(hangve_id)).first()


def load_chuyen_bay(tuyen_bay_id=None, khoihanh=None):
    datetime_string_format = '%Y-%m-%d'
    khoihanhdatetime = datetime.strptime(khoihanh, datetime_string_format)

    today = datetime.now()
    newdate = today + timedelta(hours=12)

    if tuyen_bay_id and khoihanh:
        return ChuyenBay.query.filter(ChuyenBay.ma_tuyen_bay.__eq__(tuyen_bay_id),
                                      (ChuyenBay.sl_ghe_hang1 + ChuyenBay.sl_ghe_hang2) > 0,
                                      extract('month', ChuyenBay.ngay_gio) == khoihanhdatetime.month,
                                      extract('year', ChuyenBay.ngay_gio) == khoihanhdatetime.year,
                                      extract('day', ChuyenBay.ngay_gio) == khoihanhdatetime.day,
                                      newdate < ChuyenBay.ngay_gio)

    return ChuyenBay.all()


def load_chuyen_bay2(chuyenbay_name=None, timebay=None):
    today = datetime.now()
    newdate = today + timedelta(hours=4)

    chuyenbay = ChuyenBay.query.filter((ChuyenBay.sl_ghe_hang1 + ChuyenBay.sl_ghe_hang2) > 0,
                                       newdate < ChuyenBay.ngay_gio)

    if chuyenbay_name:
        chuyenbay = chuyenbay.filter(ChuyenBay.name.__eq__(chuyenbay_name))

    if timebay:
        chuyenbay = chuyenbay.filter(ChuyenBay.thoi_gian_bay.__eq__(timebay))

    return chuyenbay.all()


def check_tuyen_bay(san_bay_di_id, san_bay_den_id):
    if san_bay_di_id and san_bay_den_id:

        return TuyenBay.query.filter(TuyenBay.ma_san_bay_di.__eq__(san_bay_di_id.strip()),
                                     TuyenBay.ma_san_bay_den.__eq__(san_bay_den_id)).first()


def check_chuyen_bay(tuyen_bay_id):
    if tuyen_bay_id:

        return ChuyenBay.query.filter(ChuyenBay.ma_tuyen_bay.__eq__(tuyen_bay_id)).first()


def check_user(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_san_bay_by_id(sanbay_id):
    return SanBay.query.get(sanbay_id)


def get_tuyen_bay_by_id(tuyenbay_id):
    return TuyenBay.query.get(tuyenbay_id)


def get_chuyen_bay_by_id(chuyenbay_id):
    return ChuyenBay.query.get(chuyenbay_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def add_chuyenbay(chuyenbayname, ngaygio, thoigianbay, slghehang1, slghehang2,
                  sanbaytrunggian, thoigiandung, ghichu, matuyenbay):
    cb = ChuyenBay(name=chuyenbayname, ngay_gio=ngaygio, thoi_gian_bay=thoigianbay, sl_ghe_hang1=slghehang1,
                   sl_ghe_hang2=slghehang2, san_bay_trung_gian=sanbaytrunggian, thoi_gian_dung=thoigiandung,
                   ghi_chu=ghichu, ma_tuyen_bay=matuyenbay)
    db.session.add(cb)
    db.session.commit()


def add_rule(slsanbay, slhangve, sanbaytrunggianmax, timebaymin, timedungmin, timedungmax, timebanve, timedatve):
    rule = Rule(sl_sanbay=slsanbay, sl_hang_ve=slhangve, san_bay_trung_gian_max=sanbaytrunggianmax,
                time_bay_min=timebaymin, time_dung_min=timedungmin, time_dung_max=timedungmax,
                time_ban_ve=timebanve, time_dat_ve=timedatve)
    db.session.add(rule)
    db.session.commit()


def add_hoadon(cart):
    if cart:
        hoadon = HoaDon(user=current_user)
        db.session.add(hoadon)

        for c in cart.values():
            chitiet = ChiTietHoaDon(hoadon=hoadon, ma_ve=c['mave'],
                                    so_luong=c['quantity'], thanh_tien=c['gia'])

            db.session.add(chitiet)

        db.session.commit()


def add_order2(mave, soluong, thanhtien):
    hoadon = HoaDon(user=current_user)
    db.session.add(hoadon)

    d = ChiTietHoaDon(hoadon=hoadon, ma_ve=mave,
                      so_luong=soluong, thanh_tien=thanhtien)

    db.session.add(d)
    db.session.commit()


def cart_stats(cart):
    total_quantity = 0
    total_amount = 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['gia']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def tuyenbay_stats():
    return db.session.query(TuyenBay.id, TuyenBay.name, func.count(ChuyenBay.id))\
                            .join(ChuyenBay, TuyenBay.id.__eq__(ChuyenBay.ma_tuyen_bay), isouter=True)\
                            .group_by(TuyenBay.id, TuyenBay.name).all()


def stats_month(year=None):
    q = db.session.query(extract('month', HoaDon.ngay_tao), TuyenBay.name,
                         func.sum(ChiTietHoaDon.so_luong * ChiTietHoaDon.thanh_tien))\
                    .join(ChiTietHoaDon, ChiTietHoaDon.ma_hoa_don.__eq__(HoaDon.id))\
                    .join(Ve, Ve.id.__eq__(ChiTietHoaDon.ma_ve))\
                    .join(ChuyenBay, ChuyenBay.id.__eq__(Ve.ma_chuyen_bay))\
                    .join(TuyenBay, TuyenBay.id.__eq__(ChuyenBay.ma_tuyen_bay))\
                    .group_by(extract('month', HoaDon.ngay_tao), TuyenBay.name)\
                    .order_by(extract('month', HoaDon.ngay_tao))

    if year:
        q = q.filter(extract('year', HoaDon.ngay_tao) == year)

    return q.all()
