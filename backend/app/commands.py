import click
from . import app, db
from .models import Student, Admin, Building


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
    student = Student(no="1950001",
                      name="刃心",
                      password="123456",
                      gender="男",
                      major="数据库",
                      grade=2019,
                      classno=1,
                      profile="我太帅了",
                      tel="12345679999",
                      email="renxin-ty@qq.com",
                      building_id=1)  # 主键从1开始

    admin = Admin(no="123",
                  name="管理",
                  role=0,
                  password="123",
                  tel="12345678910",
                  email="guan@li.com")

    admin1 = Admin(no="1234",
                   name="管理",
                   password="123",
                   tel="12345678910",
                   email="guan@li1.com",
                   building_id=1)

    building = Building(name="友园7号楼",
                        gender='男',
                        is_bed_on_table=True,
                        is_independent_bathroom=True,
                        profile="楼里全是帅哥")

    try:
        db.session.add_all([student, admin, admin1, building])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(e)
    else:
        click.echo("创建成功")
