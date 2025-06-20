import sys
print("-----")
print(sys.path)
print("------2")
from billSplitter import create_app, db
from billSplitter.models import *

with app.app_context():
    db.create_all()
    print("✅ Database tables created.")