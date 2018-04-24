#coding=utf-8
'''输入的数据都需要通过Form提交处理，所以form类的建立要有逻辑。决定将公司注册的页面表格单独拿出来，
RegisterCompanyForm表中也不一定要将Company表中所有信息列为必填项，挑几个必填，然后建立CompanyForm,创建公司信息更新函数进行数据更新
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from jobplus.models import db, User, Company, Job


class RegisterCompanyForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    com_website = StringField('网站地址', validators=[Required(), URL()])
    logo_url = StringField('公司logo') #没有实现图片上传功能，这里注册的时候可以不填，使用爬到的url地址
    com_shotinfo = TextAreaField('一句话简介', validators=[Required(), Length(1, 30)])
    com_description = TextAreaField('公司详细介绍', validators=[Required(), Length(20, 400)])
    com_adress = StringField('地址',validators=[Required()]) #对这几个field的类型还需要具体了解
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交') 

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('公司已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    role=20) #role设置为20即企业用户
        company = Company(user_id=user.id,
        	              companyname=self.username.data,
        	              com_website=self.com_website.data,
                          logo_url=self.logo_url.data,
                          com_shortinfo=self.com_shotinfo.data,
                          com_description=self.com_description.data,
                          com_address=self.com_adress.data) #通过id将user和company表一对一关联起来，这里面logo_url要是空的话不知是否会出错，company=Company() self.populate_obj(company)如出错可以换用这个形式填充
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        return user

#这个就是指一般用户即求职者的注册，role默认设置成了10也即一般用户
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交') 

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


    def create_user(self):
        user = User(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data) #不用重新设置，默认就是我们需要的值
        db.session.add(user)
        db.session.commit()
        return user

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交') 

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
