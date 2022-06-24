import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.qq.com")  # 暂时使用QQ邮箱
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS",
                                  "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[DormSys]"
    FLASKY_MAIL_SENDER = "DormSys Admin <1595606114@qq.com>"
    # 设置sqlalchemy不自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO",
                                     "true").lower() in ["true", "on", "1"]
    # 禁止自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    JSON_AS_ASCII = False

    REDIS_URL = os.environ.get("REDIS_URL") or "redis:///localhost:6379/1"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL") or "sqlite:///" + os.path.join(
            basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
