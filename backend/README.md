# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
API REFERENCE

GETTING STARTED

Base URL: The app can currently only be run locally; the backend is hosted at http://127.0.0.1:5000/ (configured as a proxy in the frontend's package.json )
Authentication: The current version of the app does not require any authentication.

ERROR HANDLING

Errors are returned in the following JSON format:

{
  "success": False,
  "error": 422,
  "message": "Unprocessable"
}

The API may return the following errors:

400: Bad request
404: Not found
405: Method not allowed
422: Unprocessable
500: Server error

ENDPOINTS

GET /categories

General: Returns a success value and a category object in JSON format
Sample: curl http://127.0.0.1:5000/categories

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

GET /questions

General:
- Returns a success value, a list of paginated question objects (in groups of 10), total questions, categories, and the current category in JSON format
- Page number can be indicated with a query string at the end of the endpoint (e.g. /questions?page=3)
Sample: curl http://127.0.0.1:5000/questions  

{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ***SEVEN MORE QUESTION OBJECTS TO COMPLETE GROUP OF TEN***
    ],
    "success": true,
    "total_questions": 18
}

POST /questions

General:
- This endpoint has two functionalities:
    1) To search for questions by question body (i.e. not by a question's answer or difficulty) using the submitted "searchTerm" (searches are case insensitive and return all results containing the submitted search term)
      - Returns a success value, a list of paginated matching question objects (in groups of 10), total matching questions, and the current category in JSON format
    2) To create a new question using the submitted question, answer, difficulty and category.
      - Returns a success value and the submitted question (with its newly created id) in JSON format

Sample:
1) To search for questions:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Dutch"}'

{
    "current_category": null,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 1
}

2) To create a new question:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "How many provinces are there in Costa Rica?", "answer": "seven", "difficulty": 3, "category": 3}'

{
    "question": {
        "answer": "seven",
        "category": 3,
        "difficulty": 3,
        "id": 29,
        "question": "How many provinces are there in Costa Rica?"
    },
    "success": true
}

DELETE /questions/<question_id>

General:
- Deletes a question by using question_id, which is submitted in the query string
- Returns a success value and the deleted question object in JSON format

Sample: curl http://127.0.0.1:5000/questions/29 -X DELETE   

{
    "question": {
        "answer": "seven",
        "category": 3,
        "difficulty": 3,
        "id": 29,
        "question": "How many provinces are there in Costa Rica?"
    },
    "success": true
}


GET /categories/<category_id>/questions

General:
- Returns a success value, a list of the submitted category's question objects (paginated in groups of 10), the total number of questions for the provided category, and the current category id in JSON format
- The category_id is submitted via the query string

Sample: curl http://127.0.0.1:5000/categories/2/questions

{
    "current_category": "2",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 4
}


POST /quizzes

General:
- Takes the "quiz_category" object containing the question id (or '0' for all questions) and the question type (or "None" for all questions), as well as a list of previous question ids ("previous_questions")
- Returns a success value and a new question from the submitted category whose id does not already form part of the list of previous question ids
- If there are no more questions available for a given category, "None" is returned as the question value, which ends the trivia game

Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16, 17], "quiz_category": {"type": "Art", "id": 2}}'

{
    "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    "success": true
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
