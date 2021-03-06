#coding=utf-8
import sys
from flask import Flask
from flask_migrate import Migrate
from jobplus.config import configs
from jobplus.models import db, User
from flask_login import LoginManager

#reload(sys)
#sys.setdefaultencoding('utf-8') #在windows环境下编写的代码在linux上运行会出现编码错误，加上这几句就不会报错了

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'



def register_blueprints(app):
    from .handlers import front, job, admin, user, company
    app.register_blueprint(front)
    app.register_blueprint(job)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(company)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    
    register_extensions(app) 
    register_blueprints(app)
     
    return app
