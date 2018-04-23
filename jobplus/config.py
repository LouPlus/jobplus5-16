class BaseConfig(object):
	SECRET_KEY = 'louplus 5-16'
	INDEX_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/jobplus?charset=utf8'

class ProductionConfig(DevelopmentConfig):
	DEBUG = False

class TestingConfig(BaseConfig):
	pass

configs = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'testing': TestingConfig
}
