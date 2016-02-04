from app import app
from app.Views.views import render

@app.route('/home')
def homejobseekers():
    return render('homejobseekers.html', extra='homejobseekers')
