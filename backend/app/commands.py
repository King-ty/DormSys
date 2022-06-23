import click
from . import app, db
from .models import Student


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest

    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def db_init():
    """创建数据库"""
    db.drop_all()
    db.create_all()
    student = Student(
        no="1950001",
        name="刃心",
        password="123456",
        gender="M",
        major="数据库",
        grade=2019,
        classno=1,
        profile="我太帅了",
        tel="12345679999",
    )

    db.session.add(student)
    db.session.commit()

    click.echo("创建成功")
