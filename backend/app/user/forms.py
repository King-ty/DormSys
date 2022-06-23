from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

from ..models import Student, Admin


class LoginForm(FlaskForm):
    no = StringField(
        "学号",
        validators=[DataRequired(), Length(1, 9), Regexp(r"^\d*$", 0, "学号必须是数字字符串")],
    )
    password = PasswordField("密码", validators=[DataRequired()])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("旧密码", validators=[DataRequired()])
    password = PasswordField(
        "新密码", validators=[DataRequired(), EqualTo("password2", message="两次输入密码必须相同！")]
    )
    password2 = PasswordField("重新输入新密码", validators=[DataRequired()])
    submit = SubmitField("确认")

