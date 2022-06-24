from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User:
    no = db.Column(db.String(16), primary_key=True, index=True)
    name = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # 存储加密字符串
    gender = db.Column(db.String(1))  # 可空
    tel = db.Column(db.String(20))
    email = db.Column(db.String(64), unique=True)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(User, db.Model):
    __tablename__ = "students"

    role = db.Column(db.SmallInteger, default=2, nullable=False)
    major = db.Column(db.String(32))
    grade = db.Column(db.SmallInteger)  # eg:2019
    classno = db.Column(db.SmallInteger)  # eg:1
    profile = db.Column(db.Text)

    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    dorm_id = db.Column(db.Integer, db.ForeignKey("dormitories.id"))

    def __repr__(self):
        return "<Student %r>" % self.name


class Admin(User, db.Model):
    __tablename__ = "administrators"

    role = db.Column(db.SmallInteger, default=1, nullable=False)

    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))

    def __repr__(self):
        return "<Administrator %r>" % self.name


class Building(db.Model):
    __tablename__ = "buildings"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    is_bed_on_table = db.Column(db.Boolean, default=False)
    is_independent_bathroom = db.Column(db.Boolean, default=False)
    profile = db.Column(db.Text)

    students = db.relationship("Student", backref="building", lazy="dynamic")
    admins = db.relationship("Admin", backref="building", lazy="dynamic")
    dormitories = db.relationship("Dormitory",
                                  backref="building",
                                  lazy="dynamic")

    def __repr__(self):
        return "<Building %r>" % self.name


class Dormitory(db.Model):
    __tablename__ = "dormitories"

    id = db.Column(db.Integer, primary_key=True)  # 额外抽象出一个主键
    no = db.Column(db.String(10))
    max_number = db.Column(db.SmallInteger, default=4, nullable=False)

    building_id = db.Column(db.Integer, db.ForeignKey("buildings.id"))
    students = db.relationship("Student", backref="dormitory", lazy="dynamic")

    def __repr__(self):
        return "<Dormitory %r>" % (self.building_id + "-" + self.no)


class Score(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    dorm_id = db.Column(db.Integer,
                        db.ForeignKey("dormitories.id"),
                        primary_key=True)
    work_no = db.Column(db.String(16),
                        db.ForeignKey("administrators.no"),
                        primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    score = db.Column(db.SmallInteger, nullable=False)
    check_type = db.Column(db.SmallInteger, nullable=False)  # TODO:编写枚举类型代表检查
    profile = db.Column(db.Text)

    def __repr__(self):
        return "<Score %r>" % ("宿舍ID：" + self.dorm_id + " 工号：" + self.work_no +
                               " 时间：" + self.time)


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    stu_no = db.Column(db.String(16),
                       db.ForeignKey("students.no"),
                       primary_key=True,
                       index=True)
    propose_time = db.Column(db.DateTime, primary_key=True)
    req_type = db.Column(db.SmallInteger, nullable=False)  # TODO:编写枚举类型代表请求
    content = db.Column(db.Text, nullable=False)
    handle_time = db.Column(db.DateTime)
    handle_profile = db.Column(db.Text)

    def __repr__(self):
        return "<Request %r>" % ("学号：" + self.stu_no + " 提出时间：" +
                                 self.propose_time)


class Notice(db.Model):
    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)
    work_no = db.Column(db.String(16),
                        db.ForeignKey("administrators.no"),
                        primary_key=True,
                        index=True)
    notice_time = db.Column(db.DateTime, primary_key=True)
    notice_type = db.Column(db.SmallInteger, nullable=False)  # TODO:编写枚举类型代表公告
    content = db.Column(db.Text, nullable=False)

    # profile = db.Column(db.Text)

    def __repr__(self):
        return "<Notice %r>" % ("工号：" + self.work_no + " 发布时间：" +
                                self.notice_time)


class Violation(db.Model):
    __tablename__ = "violations"

    id = db.Column(db.Integer, primary_key=True)
    stu_no = db.Column(db.String(16),
                       db.ForeignKey("students.no"),
                       primary_key=True,
                       index=True)
    violate_time = db.Column(db.DateTime, primary_key=True)
    violate_type = db.Column(db.SmallInteger,
                             nullable=False)  # TODO:编写枚举类型代表违纪
    profile = db.Column(db.Text)

    def __repr__(self):
        return "<Notice %r>" % ("学号：" + self.stu_no + " 违纪时间：" +
                                self.violate_time + " 违纪类型：" +
                                self.violate_type)


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    stu_no = db.Column(db.String(16),
                       db.ForeignKey("students.no"),
                       primary_key=True,
                       index=True)
    pay_time = db.Column(db.DateTime, primary_key=True)
    pay_type = db.Column(db.SmallInteger, nullable=False)  # TODO:编写枚举类型代表违纪
    amount = db.Column(db.Integer, nullable=False)
    profile = db.Column(db.Text)

    def __repr__(self):
        return "<Notice %r>" % ("学号：" + self.stu_no + " 缴费时间：" +
                                self.pay_time + " 缴费类型：" + self.pay_type)
