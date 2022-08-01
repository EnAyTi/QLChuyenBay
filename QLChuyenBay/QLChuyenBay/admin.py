import utils
from datetime import datetime
from flask import redirect, request
from flask_admin import Admin
from QLChuyenBay import db, app
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask_admin import BaseView, expose, AdminIndexView
from QLChuyenBay.models import TuyenBay, ChuyenBay, UserRole, Rule


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class CompelLogin(ModelView):
    can_view_details = True
    details_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):

        return self.render('admin/index.html', stats=utils.tuyenbay_stats())


class TuyenBayView(CompelLogin):
    column_filters = ['ma_san_bay_di', 'ma_san_bay_den']
    column_searchable_list = ['name']
    column_labels = {
        'san_bay_di': 'Sân bay đi',
        'san_bay_den': 'Sân bay đến',
        'name': 'Tên tuyến bay',
        'chuyen_bay': 'Chuyến bay'
    }


class ChuyenBayView(CompelLogin):
    column_filters = ['name']
    column_searchable_list = ['name', 'ma_tuyen_bay']
    column_labels = {
        'id': 'Mã chuyến',
        'name': 'Tên chuyến',
        'ngay_gio': 'Ngày giờ',
        'thoi_gian_bay': 'Thời gian bay',
        'sl_ghe_hang1': 'Số lượng ghế hạng 1',
        'sl_ghe_hang2': 'Số lượng ghế hạng 2',
        'sanbaytrunggian': 'Sân bay trung gian',
        'thoi_gian_dung': 'Thời gian dừng',
        'ghi_chu': 'Ghi chú',
        'ma_tuyen_bay': 'Tuyến bay',
        'tuyenbay': 'Tuyến bay',
    }
    column_sortable_list = ['name', 'thoi_gian_bay']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        year = request.args.get('year', datetime.now().year)
        stats = utils.stats_month(year=year)
        return self.render('/admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ChangeRule(BaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        if request.method.__eq__('POST'):
            slsanbay = request.form.get('slsanbay')
            slhangve = request.form.get('slhangve')
            sanbaytrunggianmax = request.form.get('sanbaytrunggianmax')
            timebaymin = request.form.get('timebaymin')
            timedungmin = request.form.get('timedungmin')
            timedungmax = request.form.get('timedungmax')
            timebanve = request.form.get('timebanve')
            timedatve = request.form.get('timedatve')

            rule = Rule.query.filter(Rule.id.__eq__(1)).first()
            if rule:
                rule.sl_sanbay = int(slsanbay)
                rule.sl_hang_ve = int(slhangve)
                rule.san_bay_trung_gian_max = int(sanbaytrunggianmax)
                rule.time_bay_min = timebaymin
                rule.time_dung_min = timedungmin
                rule.time_dung_max = timedungmax
                rule.time_ban_ve = timebanve
                rule.time_dat_ve = timedatve
                db.session.add(rule)
                db.session.commit()
                return redirect('/admin')
            else:
                utils.add_rule(slsanbay=slsanbay, slhangve=slhangve, sanbaytrunggianmax=sanbaytrunggianmax,
                               timebaymin=timebaymin, timedungmin=timedungmin, timedungmax=timedungmax,
                               timebanve=timebanve, timedatve=timedatve)
        return self.render('admin/changerule.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class BanVe(BaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        err_msg = ''
        chuyenbay_name = request.args.get('chuyenbay_name')
        timebay = request.args.get('timebay')
        chuyenbays = utils.load_chuyen_bay2(chuyenbay_name=chuyenbay_name, timebay=timebay)
        if request.method == 'post':
            cbname = request.form.get('cbname')
            hangve = request.form.get('hangve')
            soluong = request.form.get('soluong')

            cb_id = ChuyenBay.query.filter(ChuyenBay.name.__eq__(cbname)).first()

            if cb_id:
                ve2 = utils.load_ve2(chuyenbay_id=cb_id.id, hangve_id=hangve)
                thanhtien = soluong * ve2.hangve.gia
                utils.add_order2(mave=ve2.id, soluong=soluong, thanhtien=thanhtien)
                return redirect('/admin')
            else:
                err_msg = 'Đã có lỗi xảy ra'
        return self.render('admin/banve.html', chuyenbays=chuyenbays, err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


class LichChuyenBay(BaseView):
    @expose('/', methods=['get', 'post'])
    def index(self):
        err_msg = ''
        if request.method.__eq__('POST'):
            chuyenbayname = request.form.get('chuyenbayname')
            ngaygio = request.form.get('ngaygio')
            thoigianbay = request.form.get('thoigianbay')
            slghehang1 = int(request.form.get('slghehang1'))
            slghehang2 = int(request.form.get('slghehang2'))
            sanbaytrunggian = request.form.get('sanbaytrunggian')
            thoigiandung = request.form.get('thoigiandung')
            ghichu = request.form.get('ghichu')
            matuyenbay = request.form.get('matuyenbay')

            datetime_string_format = '%H:%M'
            thoigianbaydatetime = datetime.strptime(thoigianbay, datetime_string_format)
            if not thoigiandung and not sanbaytrunggian:
                rule = Rule.query.filter(Rule.id.__eq__(1)).first()
                a = rule.time_bay_min

                if thoigianbaydatetime.time() <= a:
                    err_msg = 'Thời gian bay tối thiểu là {}'.format(a)
                else:
                    utils.add_chuyenbay(chuyenbayname=chuyenbayname, ngaygio=ngaygio, thoigianbay=thoigianbay,
                                        slghehang1=slghehang1, slghehang2=slghehang2, sanbaytrunggian=None,
                                        thoigiandung=None, ghichu=ghichu, matuyenbay=matuyenbay)
                    return redirect('/admin')
            else:
                thoigiandungdatetime = datetime.strptime(thoigiandung, datetime_string_format)

                rule = Rule.query.filter(Rule.id.__eq__(1)).first()
                a = rule.time_bay_min
                c = rule.time_dung_min
                d = rule.time_dung_max

                if thoigianbaydatetime.time() <= a:
                    err_msg = 'Thời gian bay tối thiểu là {}'.format(a)
                elif thoigiandungdatetime.time() < c or thoigiandungdatetime.time() > d:
                    err_msg = 'Thời gian dừng từ {} đến {}'.format(c, d)
                else:
                    utils.add_chuyenbay(chuyenbayname=chuyenbayname, ngaygio=ngaygio, thoigianbay=thoigianbay,
                                        slghehang1=slghehang1, slghehang2=slghehang2, sanbaytrunggian=sanbaytrunggian,
                                        thoigiandung=thoigiandung, ghichu=ghichu, matuyenbay=matuyenbay)
                    return redirect('/admin')

        return self.render('admin/lap-lich-chuyen-bay.html', err_msg=err_msg)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.EMPLOYEE


admin = Admin(app=app, name='QUẢN TRỊ CHUYẾN BAY', template_mode='bootstrap4', index_view=MyIndexView())
admin.add_view(TuyenBayView(TuyenBay, db.session, name='Tuyến bay'))
admin.add_view(ChuyenBayView(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(ChangeRule(name="Thay đổi quy định"))
admin.add_view(BanVe(name="Bán vé"))
admin.add_view(LichChuyenBay(name="Lập lịch chuyến bay"))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
