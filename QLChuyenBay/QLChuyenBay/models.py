from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin
from QLChuyenBay import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    EMPLOYEE = 2
    USER = 3


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/defaultava.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    hoa_don = relationship('HoaDon', backref='user', lazy=True)

    def __str__(self):
        return self.name


class SanBay(BaseModel):
    ma_san_bay = Column(String(50), nullable=False, unique=True)
    ten_thanh_pho = Column(String(50), nullable=False)
    chuyen_bay = relationship('ChuyenBay', backref='sanbaytrunggian', lazy=True)

    def __str__(self):
        return self.ma_san_bay


class TuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    ma_san_bay_di = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    ma_san_bay_den = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    active = Column(Boolean, default=True)

    san_bay_di = relationship("SanBay", foreign_keys=[ma_san_bay_di])
    san_bay_den = relationship("SanBay", foreign_keys=[ma_san_bay_den])
    chuyen_bay = relationship('ChuyenBay', backref='tuyenbay', lazy=True)

    def __str__(self):
        return self.name


class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    ngay_gio = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(Time, nullable=False)
    sl_ghe_hang1 = Column(Integer, nullable=False)
    sl_ghe_hang2 = Column(Integer, nullable=False)
    san_bay_trung_gian = Column(Integer, ForeignKey(SanBay.id))
    thoi_gian_dung = Column(Time)
    ghi_chu = Column(String(255))
    ma_tuyen_bay = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    ve = relationship('Ve', backref='chuyenbay', lazy=True)

    def __str__(self):
        return self.name


class HangVe(BaseModel):
    ten = Column(String(50))
    gia = Column(Float, default=0, nullable=False)
    ve = relationship('Ve', backref='hangve', lazy=True)


class Ve(BaseModel):
    ma_chuyen_bay = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    ma_hang_ve = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    chi_tiet_hoa_don = relationship('ChiTietHoaDon', backref='ve', lazy=True)


class HoaDon(BaseModel):
    ngay_tao = Column(DateTime, default=datetime.now())
    ma_user = Column(Integer, ForeignKey(User.id), nullable=False)
    chi_tiet_hoa_don = relationship('ChiTietHoaDon', backref='hoadon', lazy=True)


class ChiTietHoaDon(db.Model):
    ma_hoa_don = Column(Integer, ForeignKey(HoaDon.id), nullable=False, primary_key=True)
    ma_ve = Column(Integer, ForeignKey(Ve.id), nullable=False, primary_key=True)
    so_luong = Column(Integer, default=0)
    thanh_tien = Column(Float, default=0)


class Rule(BaseModel):
    sl_sanbay = Column(Integer, nullable=False)
    sl_hang_ve = Column(Integer, nullable=False)
    san_bay_trung_gian_max = Column(Integer, nullable=False)
    time_bay_min = Column(Time, nullable=False)
    time_dung_min = Column(Time, nullable=False)
    time_dung_max = Column(Time, nullable=False)
    time_ban_ve = Column(Time, nullable=False)
    time_dat_ve = Column(Time, nullable=False)


if __name__ == "__main__":
    db.create_all()

    sanbay = [{
        "ma_san_bay": "HAN",
        "ten_thanh_pho": "Hà Nội"
    }, {
        "ma_san_bay": "HPH",
        "ten_thanh_pho": "Hải Phòng"
    }, {
        "ma_san_bay": "DIN",
        "ten_thanh_pho": "Điện Biên Phủ"
    }, {
        "ma_san_bay": "THD",
        "ten_thanh_pho": "Thanh Hóa"
    }, {
        "ma_san_bay": "VII",
        "ten_thanh_pho": "Vinh"
    }, {
        "ma_san_bay": "VDH",
        "ten_thanh_pho": "Đồng Hới"
    }, {
        "ma_san_bay": "HUI",
        "ten_thanh_pho": "Huế"
    }, {
        "ma_san_bay": "DAD",
        "ten_thanh_pho": "Đà Nẵng"
    }, {
        "ma_san_bay": "VCL",
        "ten_thanh_pho": "Quảng Nam"
    }, {
        "ma_san_bay": "UIH",
        "ten_thanh_pho": "Qui Nhơn"
    }]

    for s in sanbay:
        san = SanBay(ma_san_bay=s['ma_san_bay'], ten_thanh_pho=s['ten_thanh_pho'])
        db.session.add(san)

    db.session.commit()
