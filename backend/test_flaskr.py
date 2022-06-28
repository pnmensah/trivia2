import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres',
                                                  'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'What is the best color?',
            'answer': 'Blue',
            'category': 2,
            'difficulty': 1
        }
        self.new_category = {
            'type': 'Science'
        }
        self.new_quiz = {
            'previous_questions': [1, 2, 3],
            'quiz_category': {'id': 1}
        }
        self.search = {
            'searchTerm': 'What'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db=SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_per_page(self):
        res=self.client().get('/questions?page=1')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_delete_question(self):
        question=Question(question = 'What is the best food?',
                            answer = 'Pizza',
                            category = 1,
                            difficulty = 1)
        question.insert()
        question_id=question.id
        res=self.client().delete('/questions/' + str(question_id))
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)

    def test_create_question(self):
        res=self.client().post('/questions', json = self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_search_questions(self):
        res=self.client().post('/search', json = self.search)
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])   

    def test_get_questions_by_category(self):
        res=self.client().get('/categories/1/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_questions_by_category_per_page(self):
        res=self.client().get('/categories/1/questions?page=1')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_get_quiz_questions(self):
        res=self.client().post('/quizzes', json = {
            'quiz_category': {'id': 1, 'type': 'Science'},
            'previous_questions': []
        })
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_quiz_questions_per_page(self):
        res=self.client().post('/quizzes', json = {
            'quiz_category': {'id': 4, 'type': 'History'},
            'previous_questions': [5, 6]
        })
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        self.assertNotEqual(data['question']["id"], 5)
        self.assertNotEqual(data['question']["id"], 6)

        self.assertEqual(data['question']["category"], 4)

    def search_questions(self):
        res=self.client().post('/search', json = {
            'searchTerm': 'What'
        })
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_if_search_does_not_exist(self):
        res=self.client().post('/search', json = {
            'searchTerm': 'Sound'
        })
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_422_if_search_term_is_empty(self):
        res=self.client().post('/search', json = {
            'searchTerm': ''
        })
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
