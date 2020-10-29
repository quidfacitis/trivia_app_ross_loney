import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://{}:{}@{}:5432/{}'.format('rossloney', 'xochim1lc0', 'localhost', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # IMPORTANT: TO POPULATE TEST DATABASE BEFORE RUNNING TESTS, RUN "psql trivia_test < trivia.psql" FROM THE BACKEND FOLDER IN THE TERMINAL
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)

    def test_404_request_beyond_valid_page(self):
        res = self.client().get('/questions?page=800')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'zebra'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)

    def test_create_question(self):
        res = self.client().post('/questions', json={'question': 'How many provinces are there in Costa Rica?', 'answer': 'seven', 'difficulty': 3, 'category': 3})
        data = json.loads(res.data)

        question = Question.query.filter(Question.question.ilike("%Costa Rica%")).one_or_none() # ilike = case-insensitive

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(question)
        self.assertEqual(question.answer, 'seven')

        # Delete test question
        question.delete()

    def test_422_create_question_incorrect_data(self):
        res = self.client().post('/questions', json={'question': 'How many provinces are there in Costa Rica?', 'answer': 'seven', 'difficulty': 'three', 'category': 'three'})
        data = json.loads(res.data)

        question = Question.query.filter(Question.question.ilike("%Costa Rica%")).one_or_none() # ilike = case-insensitive

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)

    def test_delete_question(self):
        question = Question.query.first()
        question_id = question.id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['id'], question_id)
        self.assertEqual(data['question']['answer'], question.answer)


    def test_422_delete_question_invalid_id(self):
        res = self.client().delete('/questions/8000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), data['total_questions'])
        self.assertEqual(data['current_category'], '3')

    def test_400_get_questions_by_category_invalid_category(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_next_quiz_question_no_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': None, 'id': 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_next_quiz_question_with_previous_questions(self):
        res = self.client().post('/quizzes', json={'previous_questions': [16, 17], 'quiz_category': {'type': 'Art', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_next_quiz_question_no_more_questions_available(self):
        res = self.client().post('/quizzes', json={'previous_questions': [16, 17, 18, 19], 'quiz_category': {'type': 'Art', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], None)

    def test_400_get_next_quiz_question_invalid_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [16, 17, 18, 19], 'quiz_category': {'type': 'Coffee', 'id': 8}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
