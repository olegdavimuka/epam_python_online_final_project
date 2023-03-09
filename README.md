# Flask Boilerplate

This Flask app is a simple web service that allows to manage users, purses, transactions, currencies, and rates.
The app provides a user interface for managing these entities and also provides an API for accessing them programmatically.

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