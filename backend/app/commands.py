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
                      dorm_id=1,
                      building_id=1)  # 主键从1开始

    student2 = Student(no="1950002",
                       name="张三",
                       password="123456",
                       gender="男",
                       major="数据库",
                       grade=2019,
                       classno=1,
                       profile="我太学了",
                       tel="12345678910",
                       email="123@456.com",
                       dorm_id=1,
                       building_id=1)  # 主键从1开始

    student3 = Student(no="1950003",
                       name="李四",
                       password="123456",
                       gender="女",
                       major="数据不酷",
                       grade=2019,
                       classno=1,
                       profile="我太漂亮了",
                       tel="12345679999",
                       email="abc@edf.com",
                       dorm_id=4,
                       building_id=2)  # 主键从1开始

    admin = Admin(no="123",
                  name="管理",
                  role=0,
                  password="123",
                  tel="12345678910",
                  email="king-ty@foxmail.com")

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

    building2 = Building(name="友园9号楼",
                         gender='女',
                         is_bed_on_table=True,
                         is_independent_bathroom=True,
                         profile="楼里全是美女")

    building3 = Building(name="西南1号楼",
                         gender='男',
                         is_bed_on_table=False,
                         is_independent_bathroom=False,
                         profile="楼里全是学神")

    dormitory = Dormitory(no="201", building_id=1)
    dormitory2 = Dormitory(no="202", building_id=1)
    dormitory3 = Dormitory(no="203", building_id=1)
    dormitory4 = Dormitory(no="201", building_id=2)
    dormitory5 = Dormitory(no="202", building_id=2)

    try:
        db.session.add_all([
            student, student2, student3, admin, admin1, building, building2,
            building3, dormitory, dormitory2, dormitory3, dormitory4,
            dormitory5
        ])
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(e)
    else:
        click.echo("创建成功")
