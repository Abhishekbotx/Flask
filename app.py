#Imports

from flask import Flask,render_template,request,make_response
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy 


#My App
app = Flask(__name__)

@app.route('/')
def base():
    mylist = ['apple', 'banana', 'cherry']
    return render_template('index.html', mylist=mylist,title="Base Page")

@app.route('/other')
def other():
    return render_template('page2.html')

@app.route('/test')
def response():
    response = make_response({'message': 'hey Abhi'})
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/hi') # @app.route (rule, methods = [GET, POST])
def hello():
    return "Hello, World!"

@app.route('/greet/<name>')
def greet(name):
    return f"Hello, {name}"

@app.route('/template')
def index():
    return render_template('index.html')

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args['name']
        return f"{greeting}, {name}!"
    else:
        return "Please provide both 'greeting' and 'name' parameters in the URL."

if __name__ in "__main__":
    app.run(debug=True)