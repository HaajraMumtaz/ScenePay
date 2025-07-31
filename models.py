from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from .extensions import db
from flask_login import UserMixin
from . import login_manager
class TravelExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),name='fk_travel_user')
    group_id= db.Column(db.Integer, db.ForeignKey('group.id',name='fk_travel,grop'))
    amount = db.Column(db.Float)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(80),nullable=False)
    groups_created=db.relationship("Group",backref="Creator")
    expenses_paid = db.relationship("Expense", backref="payer")
    travel_paid = db.relationship("TravelExpense", backref="paid_by")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,name='fk_group_owner')
    num_members = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=timezone.utc)
    description = db.Column(db.String(300))
    members = db.relationship("Membership", backref="group")
    expenses = db.relationship("Expense", backref="group")
    travel_expenses = db.relationship("TravelExpense", backref="group")

class Membership(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),name='fk_membership_user',nullable=True)
    group_id=db.Column(db.Integer,db.ForeignKey('group.id'),name='fk_membership_groupr',nullable=False)
    is_guest=db.Column(db.Boolean,default=False)
    guest_name=db.Column(db.String(80))
    status=db.Column(db.String(20),default="Pending")
    joined_at=db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc))

class Expense(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    group_id=db.Column(db.Integer,db.ForeignKey("group.id"),name='fk_expense_group',nullable=False)
    title=db.Column(db.String(80),nullable=False)
    tax = db.Column(db.Float, default=0.0)
    amount=db.Column(db.Float,nullable=False)
    payer_id=db.Column(db.Integer,db.ForeignKey("user.id"),name='fk_expense_user',nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ExpenseSplit=db.relationship("ExpenseSplit",backref="TotalSpent")

class ExpenseSplit(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    expense_id=db.Column(db.Integer,db.ForeignKey("expense.id"),name='fk_split_main',nullable=True)
    guest_name = db.Column(db.String(100)) 
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),name='fk_split_user',nullable=True)
    amount=db.Column(db.Float)
    status=db.Column(db.String(20),default="unpaid")
    paid_at=db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    share = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))