from app import app
from app.Views.views import render

@app.route('/')
def home():
    return render('home.html',extra='')
