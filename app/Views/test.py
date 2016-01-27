from app import app
from app.Views.views import render
from flask.ext.login import login_required
from flask import jsonify, request

@app.route('/testajax')
def testajax():
    # Test ajax
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a+b)

@app.route('/test')
@login_required
def test():
    return render('test.html')
