# Flask Boilerplate

[![Build Status](https://app.travis-ci.com/olegdavimuka/flask_boilerplate.svg?token=dr6uXgRpCEyJcSveCLS7&branch=main)](https://app.travis-ci.com/olegdavimuka/flask_boilerplate)
[![Coverage Status](https://coveralls.io/repos/github/olegdavimuka/flask_boilerplate/badge.svg?branch=main)](https://coveralls.io/github/olegdavimuka/flask_boilerplate?branch=main)


This Flask app uses MySQL as the relational database management system for storing and managing data. SQLAlchemy is used as the high-level interface for working with the MySQL database. Alembic is used as the database migration tool for SQLAlchemy, allowing developers to manage database schema changes. Jinja2 is used as the template engine for generating dynamic web pages based on data from the database.

To use this Flask app, users should follow the installation and setup instructions provided in this readme file. Once the app is running, users can access the user interface pages for managing entities such as users, purses, transactions, currencies, and rates. The API endpoints are also available for accessing these entities programmatically.

MySQL provides a secure and reliable way to store and manage data, while SQLAlchemy and Alembic make it easier to work with the MySQL database. Jinja2 provides a powerful template engine for generating dynamic web pages based on data from the database. Overall, these technologies make it easier for developers to build and maintain complex web applications with Flask.

## Installation and Setup

To build and run the Flask app, please follow these instructions:

1. Clone the repository to your local machine:

```bash
git clone git@github.com:olegdavimuka/flask_boilerplate.git
```

2. Navigate to the project directory:

```bash
cd flask-boilerplate
```

3. Create a virtual environment:

```bash
python3 -m venv .venv
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```
5. Install the required packages:

```bash
pip install -r requirements.txt
```

6. Create the database:

```bash
flask db init
flask db migrate
flask db upgrade
```

## Usage

To start the Flask app, run the following command:

```bash
flask run
```

The app will be available at http://localhost:5000/.

The following pages are available:

- Home page: http://localhost:5000/
- Users list page: http://localhost:5000/users/
- User edit, create, and delete page: http://localhost:5000/users/<int:id>
- Purses list page: http://localhost:5000/purses/
- Purse edit, create, and delete page: http://localhost:5000/purses/<int:id>
- Transactions list page: http://localhost:5000/transactions/
- Transaction edit, create, and delete page: http://localhost:5000/transactions/<int:id>

The following API endpoints are available:

- Users list API: http://localhost:5000/api/users/
- User detail API: http://localhost:5000/api/users/<int:id>
- Purses list API: http://localhost:5000/api/purses/
- Purse detail API: http://localhost:5000/api/purses/<int:id>
- Transactions list API: http://localhost:5000/api/transactions/
- Transaction detail API: http://localhost:5000/api/transactions/<int:id>

## Testing

This Flask app uses pytest for testing. To install it, run the following command:

```bash
pip install pytest
```

To run tests, simply execute the following command from the root directory of the project:

```bash
pytest
```

The tests are located in the tests/ directory. Each file in the tests/ directory is a module that contains tests for a specific part of the app.

## Coverage

To measure the test coverage, you can use the coverage package. To install it, run the following command:

```bash
pip install coverage
```

Then, to run the tests and measure the coverage, execute the following command:

```bash
coverage run -m pytest
```

To see a report of the coverage, execute the following command:

```bash
coverage report
```

This will show you the coverage report in the terminal. If you want to generate a more detailed HTML coverage report, execute the following command:

```bash
coverage html
```
This will generate an HTML report in the htmlcov/ directory.

## Code quality tools

This Flask app uses several code quality tools to ensure that the code follows the PEP 8 style guide and is free of syntax errors and potential bugs. The tools used are:

- black: A code formatter that automatically formats the code to follow the PEP 8 style guide.
- isort: A utility that automatically sorts imports in the code.
- flake8: A code linter that checks the code for syntax errors and potential bugs.
- pylint: A code analyzer that checks the code for code smells and potential bugs.

To install these tools, run the following command:

```bash
pip install black isort flake8 pylint
```

To run these tools, you can use the following commands:

```bash
black .
isort .
flake8 .
pylint app
```

These commands will format the code, sort the imports, check the code for syntax errors and potential bugs, and analyze the code for code smells and potential bugs, respectively.

## Continuous Integration with Travis CI

This Flask app uses Travis CI for continuous integration. Travis CI is a popular continuous integration service that automatically runs tests and deploys code changes when they are pushed to the repository.

Instructions for Travis CI are provided in the .travis.yml file.

After creating this file and pushing it to your repository, Travis CI will automatically start testing your app whenever changes are pushed to the repository. Code quality and test coverage reports will also be generated automatically.

## Test Coverage with Coveralls

This Flask app uses Coveralls to track test coverage. Coveralls is a service that integrates with Travis CI (and other continuous integration services) to provide detailed test coverage reports.

Instructions for Coveralls are provided in the .coveralls.yml file.

After making changes and pushing them to your repository, Travis CI will automatically measure test coverage and send the results to Coveralls. You can view the test coverage report on the Coveralls website.