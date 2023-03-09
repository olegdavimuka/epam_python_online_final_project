from setuptools import find_packages, setup

requires = [
    "alembic==1.10.2",
    "aniso8601==9.0.1",
    "click==8.1.3",
    "Faker==17.6.0",
    "Flask==2.2.3",
    "Flask-Migrate==4.0.4",
    "Flask-RESTful==0.3.9",
    "Flask-SQLAlchemy==3.0.3",
    "Flask-WTF==1.1.1",
    "greenlet==2.0.2",
    "itsdangerous==2.1.2",
    "Jinja2==3.1.2",
    "Mako==1.2.4",
    "MarkupSafe==2.1.2",
    "python-dateutil==2.8.2",
    "pytz==2022.7.1",
    "six==1.16.0",
    "SQLAlchemy==2.0.5.post1",
    "typing_extensions==4.5.0",
    "Werkzeug==2.2.3",
    "WTForms==3.0.1",
    "astroid==2.14.2"
]

setup(
    name="e-wallet",
    version="0.1.0",
    description="A simple e-wallet application using Flask and SQLAlchemy with a MySQL database.",
    author="Oleh Davymuka",
    author_email="oleh_davymuka@epam.com",
    url="",
    packages=find_packages(),
    install_requires=requires,
    setup_requires=["flake8"],
)
