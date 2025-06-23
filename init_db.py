import sys
print("-----")
from billSplitter import create_app, db
from billSplitter.models import *
app=create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created.")