import sys
print("-----")
from billSplitter import create_app
from .extensions import db
from .models import *
app=create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created.")