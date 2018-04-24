#coding=utf-8
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from jobplus.models import User, Company, Job
from jobplus.forms import RegisterForm, LoginForm, RegisterCompanyForm
from flask_login import login_user, logout_user, login_required

front = Blueprint('front', __name__)

@front.route('/')
def index():

    return render_template('index.html')

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/registeruser', methods=['GET', 'POST'])
def user_register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form) #可以共用一个注册html页面，因为传入的form对象不同可以有不同的渲染

@front.route('/registercompany', methods=['GET', 'POST'])
def com_register():
    form = RegisterCompanyForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form) #可以共用一个注册html页面，因为传入的form对象不同可以有不同的渲染

@front.route('/job')
def job():
	#这里是不是可以使用job(page)的形式
    page = request.args.get('page', default=1, type=int) #page是jinja模板中传入的参数，get方式过来的，从request中获取参数
    pagination = Job.query.paginate(
	    page=page,
	    per_page=current_app.config['INDEX_PER_PAGE'],
	    error_out=False
	)
    return render_template('job.html', pagination=pagination) #在job.html中做全部职位的展示，可以考虑设置分类条件

@front.route('/company')
def company():
    page = request.args.get('page', default=1, type=int) #page是jinja模板中传入的参数，get方式过来的，从request中获取参数
    pagination = Job.query.paginate(
	    page=page,
	    per_page=current_app.config['INDEX_PER_PAGE'],
	    error_out=False
	)
    return render_template('company.html', pagination=pagination) #在company.html中做全部职位的展示，可以考虑设置分类条件,比如公司所在地等

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))
