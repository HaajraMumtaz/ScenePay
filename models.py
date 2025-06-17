from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(80),nullable=False)
    groups_created=db.relationship("Group",backref="Creator")
    expenses_paid = db.relationship("Expense", backref="payer")
    travel_paid = db.relationship("TravelExpense", backref="paid_by")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.timezone.utcnow)

    members = db.relationship("Membership", backref="group")
    expenses = db.relationship("Expense", backref="group")
    travel_expenses = db.relationship("TravelExpense", backref="group")

class Membership(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    group_id=db.Column(db.Integer,db.ForeignKey('group.id'),nullable=False)
    is_guest=db.Column(db.Boolean,default=False)
    guest_name=db.Column(db.String(80))
    status=db.Column(db.String(20),default="Pending")
    joined_at=db.Column(db.DateTime,default=datetime.timezone.utcnow)

class Expense(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    group_id=db.Column(db.Integer,db.ForeignKey("group.id"),nullable=False)
    title=db.Column(db.String(80),nullable=False)
    amount=db.Column(db.Float,nullable=False)
    payer_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.timezone.utcnow)
    ExpenseSplit=db.relationship("ExpenseSplit",backref="TotalSpent")

class ExpenseSplit(db.Model):
    expense_id=db.Column(db.Integer,db.ForeignKey("expense.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    amount=db.Column(db.Float)
    status=db.Column(db.String(20),default="unpaid")
    paid_at=db.Column(db.DateTime, default=datetime.timezone.utcnow)

