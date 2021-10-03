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
        self.database_path = "postgres://{}:{}@{}/{}".format('myuser','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
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
    def test_retrieve_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_retrieve_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])
    
    def test_search_questions(self):
        res = self.client().post("/questions", json={"searchTerm": "country"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["totalQuestions"], 1)
        first_question = data["questions"][0]
        self.assertEqual(first_question["answer"], "Uruguay")
        self.assertEqual(first_question["category"], 6)
        self.assertEqual(first_question["difficulty"], 4)
        self.assertEqual(first_question["id"], 11)
        self.assertEqual(first_question["question"], "Which country won the first ever soccer World Cup in 1930?")
    
    def test_create_question(self):
        res = self.client().post(
            "/questions",\
            json={
                "question": "Test question",
                "answer": "Test answer",
                "category": 1,
                "difficulty": 1
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()