from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True #声明不是model类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30
     
    #求职者，管理员，公司共有的几个必须字段 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    #设置企业ID关联到Company表中，设置外键，建立一对一关系，获取企业具体信息
    #RegisterCompanyForm中要将输入信息存入到user和company表中并建立联系
    com_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE")) 
    com_info = db.relationship('Company', uselist=False, backref='com_user') #这个backref可以从company访问到公司用户对象，可能用不上

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY
    @property
    def is_user(self):
    	return self.role == self.ROLE_USER


class Company(Base):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(32), unique=True, index=True, nullable=False) #要与关联的username一致，暂时先设置这个字段
    logo_url = db.Column(db.String(256)) #公司logo
    com_website = db.Column(db.String(256)) #公司网站
    com_shortinfo = db.Column(db.String(256)) #一句话简介
    com_description = db.Column(db.String(512)) #详细描述
    com_address = db.Column(db.String(32)) #公司地点
    comrecruit_num = db.Column(db.Integer) #招聘岗位数量
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete="CASCADE")) #将公司和他招聘的岗位联系起来
    recruit_jobs = db.relationship('Job') #公司招聘的岗位列表

    def __repr__(self):
        return '<Company:{}>'.format(self.companyname)

class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(32), index=True, nullable=False)
    salary_up = db.Column(db.Integer) #设置薪水的上下限
    salary_down = db.Column(db.Integer)
    exper_need = db.Column(db.String(32)) #经验要求
    work_address = db.Column(db.String(32)) #工作地点
    job_need = db.Column(db.String(128)) #职位要求
    job_description = db.Column(db.String(256)) #职位描述
    #继承了Base基类，Base类里定义了发布时间created_at和更新时间updated_at，需要显示在前端的话可以直接调用
    recruit_company = db.relationship('Company', uselist=False) #岗位和公司是多对一，一个具体的岗位就对应一个具体公司


    def __repr__(self):
        return '<Job:{}>'.format(self.jobname)


