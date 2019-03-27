# services/users/manage.py
import unittest

from flask.cli import FlaskGroup

import coverage

from project import create_app, db
from project.api.models import User

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py"]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database"""
    db.session.add(User(username="michael", email="michaeljohn@rsu.edu"))
    db.session.add(User(username="henry", email="henrybirns@gmail.com"))
    db.session.commit()


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        print("Test Completed")
        return 0
    print("Test NOT Completed")
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage"""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()
