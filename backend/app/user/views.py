from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import user
from .. import db
from ..models import Student
from .forms import LoginForm, ChangePasswordForm


@user.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = Student.query.filter_by(no=form.no.data).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("错误的学号或密码")
    return render_template("user/login.html", form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    flash("您已成功登出！")
    return redirect(url_for("main.index"))


@user.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("修改密码成功")
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        else:
            flash("原密码输入错误")
    return render_template("user/change_password.html", form=form)

