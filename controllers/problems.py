from curses.ascii import HT
from http import HTTPStatus

# ! import g
from flask import Blueprint, request, g
from marshmallow.exceptions import ValidationError
from models.problem import ProblemModel
from serializers.problem import ProblemSchema
from models.advice import AdviceModel
from serializers.advice import AdviceSchema

from middleware.secure_route import secure_route

problem_schema = ProblemSchema()
advice_schema = AdviceSchema()

router = Blueprint("problems", __name__)

#GET ALL PROBLEMS
@router.route("/problems", methods=["GET"])
def get_problems():

    problems = ProblemModel.query.all()

    return problem_schema.jsonify(problems, many=True), HTTPStatus.OK

#GET SINGLE PROBLEM
@router.route("/problems/<int:problem_id>", methods=["GET"])
def get_single_problem(problem_id):

    problem = ProblemModel.query.get(problem_id)

    if not problem:
        return {"message": "Problem not found"}, HTTPStatus.NOT_FOUND

    return problem_schema.jsonify(problem), HTTPStatus.OK

#CREATE PROBLEMS
@router.route("/problems/<int:type_id>", methods=["POST"])
@secure_route
def create_problem(type_id):
    problem_dictionary = request.json

    try:
        problem = problem_schema.load(problem_dictionary)
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong" }

    problem.user_id = g.current_user.id
    problem.type_id = type_id
    problem.save()

    return problem_schema.jsonify(problem), HTTPStatus.CREATED

#EDIT PROBLEM
@router.route("/problems/<int:problem_id>", methods=["PUT"])
@secure_route
def update_problem(problem_id):
    problem_dictionary = request.json
    existing_problem = ProblemModel.query.get(problem_id)

    if not existing_problem:
        return {"message": "Tea not found"}, HTTPStatus.NOT_FOUND

    if not g.current_user.id == existing_problem.user_id:
        return {"message": "Not your tea!"}, HTTPStatus.UNAUTHORIZED

    try:
        problem = problem_schema.load(problem_dictionary, instance=existing_problem, partial=True)

    except ValidationError as e:
        return {"errors:": e.messages, "messages": "Something went wrong"}

    problem.save()

    return problem_schema.jsonify(problem), HTTPStatus.OK

#DELETE PROBLEM
@router.route("/problems/<int:problem_id>", methods=["DELETE"])
@secure_route
def remove_problem(problem_id):
    problem = ProblemModel.query.get(problem_id)

    if not problem:
        return {"message": "Problem not found"}, HTTPStatus.NOT_FOUND

    problem.remove()

    return '', HTTPStatus.NO_CONTENT
