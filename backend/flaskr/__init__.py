import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #Set up CORS and leave 'resources' parameter blank to allow "*" for origins.
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  @app.route('/categories')
  def get_categories():
      categories = Category.query.all()
      formatted_categories = {category.id: category.type for category in categories}

      if len(categories) == 0:
          abort(404)

      return jsonify({
        'success': True,
        'categories': formatted_categories
      })

  @app.route('/questions', methods=['GET', 'POST'])
  def get_and_create_questions():
      if request.method == 'GET':
          page = request.args.get('page', 1, type=int)
          start = (page - 1) * QUESTIONS_PER_PAGE
          end = start + QUESTIONS_PER_PAGE
          questions = Question.query.all()
          formatted_questions = [question.format() for question in questions]

          categories = Category.query.all()
          formatted_categories = {category.id: category.type for category in categories}

          if len(categories) == 0 or len(formatted_questions[start:end]) == 0:
              abort(404)

          return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': None
          })
      elif 'searchTerm' in request.get_json(): #POST - search
          body = request.get_json()
          search_term = body['searchTerm']

          page = request.args.get('page', 1, type=int)
          start = (page - 1) * QUESTIONS_PER_PAGE
          end = start + QUESTIONS_PER_PAGE

          questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all() # ilike = case-insensitive

          formatted_questions = [question.format() for question in questions]

          return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'current_category': None
          })
      else: # POST - create
          body = request.get_json()
          try:
              new_question = Question(question=body['question'], answer=body['answer'], difficulty=body['difficulty'], category=body['category'])
              new_question.insert()
          except:
            db.session.rollback()
            abort(422)
          finally:
            db.session.close()

          return jsonify({
            'success': True
          })

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
      try:
        question = Question.query.filter_by(id = question_id).one_or_none()
        question.delete()
      except:
        db.session.rollback()
        abort(422)
      finally:
        db.session.close()

      return jsonify({
        'success': True,
        'question': question.format()
      })


  @app.route('/categories/<category_id>/questions')
  def get_categories_by_id(category_id):
      if int(category_id) < 1 or int(category_id) > 6:
          abort(400)

      questions = Question.query.filter_by(category=category_id).all()
      formatted_questions = [question.format() for question in questions]

      if len(questions) == 0:
          abort(404)

      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': len(formatted_questions),
        'current_category': category_id
      })

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
      body = request.get_json()
      previous_questions = body['previous_questions']
      category_id = body['quiz_category']['id']

      if int(category_id) < 0 or int(category_id) > 6: # the "0" is when the user selects "all categories"
          abort(400)

      questions = Question.query.filter_by(category=category_id).all() if int(category_id) > 0 else Question.query.all()
      formatted_questions = [question.format() for question in questions]

      if len(previous_questions) is 0:
          question = random.choice(formatted_questions)
          if question is None:
              abort(404)
          return jsonify({
            'success': True,
            'question': question
          })
      else:
          def filterPrevious(q):
              if q['id'] not in previous_questions:
                  return q
          filtered_questions = [q for q in formatted_questions if q['id'] not in previous_questions]
          question = None if len(filtered_questions) == 0 else random.choice(filtered_questions)
          return jsonify({
            'success': True,
            'question': question
          })

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404

  # 405 errors are automatically caught by Flask if the user tries to access an endpoint using an invalid method
  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500

  return app
