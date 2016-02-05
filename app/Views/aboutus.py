from app import app
from app.Views.views import render

@app.route('/about')
def about():
    return render('aboutus.html')
