import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.qq.com")  # 暂时使用QQ邮箱
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKY_MAIL_SUBJECT_PREFIX = "[TJ-MoralSys]"
    FLASKY_MAIL_SENDER = "TJ-MoralSys Admin <1595606114@qq.com>"
    # FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    REDIS_URL = os.environ.get("REDIS_URL") or "redis:///localhost:6379/0"

    # 定时器配置
    # 持久化配置，数据持久化至MongoDB
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(
            url="sqlite:///"
            + os.path.join(basedir, "data-dev.sqlite")
            # url="sqlite:///" + os.path.join(basedir, "jobs.sqlite")
        )
    }
    # 线程池配置，最大100个线程
    SCHEDULER_EXECUTORS = {"default": ThreadPoolExecutor(100)}
    # 调度开关开启
    # SCHEDULER_API_ENABLED = True
    # 设置容错时间为 1分钟
    SCHEDULER_JOB_DEFAULTS = {"misfire_grace_time": 60}
    # 配置时区
    SCHEDULER_TIMEZONE = "Asia/Shanghai"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
