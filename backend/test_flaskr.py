import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app
from models import setup_db, Question, Category

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(POSTGRES_USER,POSTGRES_PASSWORD,'localhost:5432', self.database_name)
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

    def test_400_create_question_w_incomplete_body(self):
        res = self.client().post(
            "/questions",\
            json={
                "question": "Test question",
                "category": 1,
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_400_create_search_questions_wo_body(self):
        res = self.client().post("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_question(self):
        # create question
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
        created_question_id = data["created"]

        # delete question
        res = self.client().delete(
            "/questions/{}".format(created_question_id)
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_failed_delete_question(self):
        res = self.client().delete(
            "/questions/{}".format(9999)
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_retrieve_category_questions(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_play_quiz_with_category_and_previous_questions(self):
        json_body = {
            "previous_questions": [1,2,3,20,21],
            "quiz_category": {
                "type" : "Science",
                "id" : 1
            }
        }
        res = self.client().post(
            "/quizzes",\
            json=json_body
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]["id"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertTrue(data["question"]["category"])
        self.assertTrue(data["question"]["difficulty"])
        self.assertTrue(data["question"]["id"] not in json_body["previous_questions"])
    
    def test_play_quiz_with_category(self):
        json_body = {
            "quiz_category": {
                "type" : "Art",
                "id" : 2
            }
        }
        res = self.client().post(
            "/quizzes",\
            json=json_body
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]["id"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertTrue(data["question"]["category"])
        self.assertTrue(data["question"]["difficulty"])

    def test_play_quiz_with_previous_questions(self):
        json_body = {
            "previous_questions": [1,2,3,20,21],
        }
        res = self.client().post(
            "/quizzes",\
            json=json_body
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]["id"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertTrue(data["question"]["category"])
        self.assertTrue(data["question"]["difficulty"])
        self.assertTrue(data["question"]["id"] not in json_body["previous_questions"])

    def test_play_quiz(self):
        json_body = {
            "previous_questions": [],
        }
        res = self.client().post(
            "/quizzes",\
            json=json_body
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]["id"])
        self.assertTrue(data["question"]["question"])
        self.assertTrue(data["question"]["answer"])
        self.assertTrue(data["question"]["category"])
        self.assertTrue(data["question"]["difficulty"])
    
    def test_400_play_quiz_without_body(self):
        res = self.client().post(
            "/quizzes"
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()