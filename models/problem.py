from app import db
from models.base import BaseModel
from models.user import UserModel
from models.advice import AdviceModel
from models.problem_advice import problem_advice


class ProblemModel(db.Model, BaseModel):

  __tablename__ = "problems"

  name = db.Column(db.Text, nullable=False, unique=True)
  diagnosis = db.Column(db.Text, nullable=False, unique=False)
  type_id = db.Column(db.Integer, db.ForeignKey("types.id"), nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

  advice = db.relationship('AdviceModel', backref='advice', secondary=problem_advice)
  user = db.relationship('UserModel', backref='users')
  
