import click
from . import app, db
from .models import Student, Admin, Building, Dormitory


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
                      building_id=1,
                      dorm_id=1)

    student2 = Student(no="1950002",
                       name="张三",
                       password="123456",
                       gender="男",
                       major="数据库",
                       grade=2019,
                       classno=1,
                       profile="我太帅了",
                       tel="12345679999",
                       email="123@qq.com",
                       building_id=1,
                       dorm_id=1)

    student3 = Student(no="1950003",
                       name="李四",
                       password="123456",
                       gender="男",
                       major="数据库",
                       grade=2019,
                       classno=1,
                       profile="我太帅了",
                       tel="12345679999",
                       email="234@qq.com",
                       building_id=1,
                       dorm_id=1)

    student4 = Student(no="1950004",
                       name="王五",
                       password="123456",
                       gender="女",
                       major="学习",
                       grade=2019,
                       classno=1,
                       profile="我太漂亮了",
                       tel="12345679999",
                       email="555@qq.com",
                       building_id=2,
                       dorm_id=4)

    admin = Admin(no="123",
                  name="管理",
                  password="123",
                  gender="男",
                  tel="12345678910",
                  email="guan@li.com",
                  role=0)

    admin2 = Admin(no="1234",
                   name="楼管",
                   password="123",
                   tel="12345678910",
                   email="lou@guan.com",
                   building_id=1)

    building = Building(name="友园7号楼",
                        gender="男",
                        is_bed_on_table=True,
                        is_independent_bathroom=True,
                        profile="楼里全帅哥")

    building2 = Building(name="友园9号楼",
                         gender="女",
                         is_bed_on_table=True,
                         is_independent_bathroom=True,
                         profile="楼里全美女")

    building3 = Building(name="西南一", gender="男", profile="楼里全学神")

    dormitory = Dormitory(no="201", building_id=1)
    dormitory2 = Dormitory(no="202", building_id=1)
    dormitory3 = Dormitory(no="203", building_id=1)
    dormitory4 = Dormitory(no="201", building_id=2)
    try:
        db.session.add_all([
            student, student2, student3, student4, admin, admin2, building,
            building2, building3, dormitory, dormitory2, dormitory3, dormitory4
        ])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(e)
    else:
        click.echo("创建成功")
