import os, sys, json, random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
      "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response


  def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods=["GET"])
  def retieve_categories():
    categories = Category.query.order_by(Category.id).all()

    if not categories:
      abort(404)
    
    categories = [category.format()['type'] for category in categories]

    return jsonify(
      {
        'success': True,
        'categories' : categories
      }
    )


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=["GET"])
  def retrieve_questions():
    # questions
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)
    
    # categories
    categories = Category.query.order_by(Category.id).all()
    
    if not categories:
      abort(404)

    categories = [category.format() for category in categories]

    formatted_categories = {}
    for category in categories:
      formatted_categories[category["id"]] = category["type"]
    
    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "totalQuestions": len(questions),
        "categories": formatted_categories,
        "currentCategory": None
      }
    )


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=["DELETE"])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
      abort(404)

    try:
      question.delete()

      return jsonify(
        {
          'success': True,
          'questionID': question_id
        }
      )
    except:
      print(sys.exc_info())
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions", methods=["POST"])
  def create_or_search_questions():
    body = request.get_json()
    # body = json.loads(request.data.decode('utf-8'))

    if not body:
      print(sys.exc_info())
      abort(400)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)
    search_term = body.get('searchTerm', None)

    if search_term:
      search_results = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')
      ).all()

      formatted_search_results = [result.format() for result in search_results]
      return jsonify(
        {
          "success": True,
          "questions": formatted_search_results,
          "totalQuestions": len(search_results),
          "currentCategory": None
        }
      )
    else:

      if (not new_question) or (not new_answer) or (not new_difficulty) or (not new_category):
        print(sys.exc_info())
        abort(400)

      try:
        new_question = Question(
          question = new_question, 
          answer = new_answer, 
          category= new_category,
          difficulty = new_difficulty
        )
        new_question.insert()

        return jsonify(
          {
            'success': True,
            'created': new_question.id
          }
        )
      except:
        print(sys.exc_info())
        abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:category_id>/questions", methods=["GET"])
  def retrieve_category_questions(category_id):
    questions = Question.\
      query.\
      filter(
        Question.category == category_id
      ).\
      order_by(Question.id).\
      all()

    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)

    category_id_name = Category.query.filter(Category.id == category_id).all()
    category_name = [category.format()['type'] for category in category_id_name][0]

    return jsonify(
      {
        'success': True,
        'questions': current_questions,
        'totalQuestions': len(questions),
        'currentCategory': category_name
      }
    )


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route("/quizzes", methods=["POST"])
  def play_quiz():
    body = request.get_json()
    # body = json.loads(request.data.decode('utf-8'))

    if not body:
      print(sys.exc_info())
      abort(400)

    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    quiz_query = Question.query

    if quiz_category:
      # Fix error in UI that reduces category if by 1
      quiz_category["id"] = int(quiz_category["id"]) + 1
      quiz_query = quiz_query.filter(Question.category == str(quiz_category['id']))
    if previous_questions:
      quiz_query = quiz_query.filter(Question.id.notin_(previous_questions))
    
    suitable_questions = quiz_query.all()

    if len(suitable_questions) == 0:
      abort(400)

    random_question = random.choice(suitable_questions)
    formatted_question = random_question.format()

    return jsonify(
      {
        "success": True,
        "question": formatted_question
      }
    )

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify(
      {
        "success": False,
        "error": 400,
        "message": "bad request"
      }
    ), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify(
      {
        "success": False,
        "error": 404,
        "message": "resource not found"
      }
    ), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify(
      {
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }
    ), 422
  
  return app

    