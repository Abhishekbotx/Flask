#Imports

from flask import Flask,render_template,request,make_response,Response,send_from_directory,session
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy 
import pandas as pd
import os
import uuid


#My App
app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/')
app.secret_key='thisisasecretkey'
@app.route('/')
def base():
    mylist = ['apple', 'banana', 'cherry']
    return render_template('index.html', mylist=mylist,title="Base Page")


    
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



@app.route('/other')
def other():
    return render_template('page2.html')



@app.route('/test')
def response():
    response = make_response({'message': 'hey Abhi'})
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    return response



@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method=='GET':
        return render_template('form.html')
    else:
        username =request.form.get('username')
        password=request.form.get('password')
        
        if username == 'Abhishek' and password == 'Raj':
            return "Logged in successfully"
        else:
            return "Invalid Credentials. Please try again."
        


@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files.get('file')  # <-- fixed
    
    if not file:
        return {"error": "No file uploaded"}, 400  # jsonify not needed here
    
    # For plain text files
    if file.content_type == 'text/plain':
        content = file.read().decode()
        return content

    # For Excel files (.xlsx or .xls)
    elif file.content_type in [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel'
    ]:
        df = pd.read_excel(file)
        return df.to_html()
    
    else:
        return "Unsupported file type", 400



@app.route('/convert_to_csv',methods=["POST"] )
def convert_to_csv():
    file = request.files.get('file') 
    
    df=pd.read_excel(file)
    response= Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={
            "Content-disposition": "attachment; filename=data.csv"
        }
    )   
    return response



@app.route('/convert_to_csv2',methods=["POST"] )
def convert_to_csv2():
    file = request.files.get('file') 
    
    df=pd.read_excel(file)
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    filename=  f'{uuid.uuid4()}.csv'
    df.to_csv(os.path.join('downloads',filename))
    return render_template('downloads.html',filename=filename)



@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('downloads',filename,download_name='result.csv')
    









@app.route('/session_and_cookies')
def sess():
    return render_template('session.html', title="Session Page",)



@app.route('/set_data')
def set_data():
    session['name'] = 'Abhishek'
    session['other'] = 'Hello World'
    return render_template(template_name_or_list='session.html', message='Session data set.')



@app.route('/get_data')
def get_data():
    if 'name' in session.keys() and 'other' in session.keys():
        name = session['name']
        other = session['other']
        return render_template(template_name_or_list='session.html', message=f'Name: {name}, Other: {other}')
    else:
        return render_template(template_name_or_list='session.html', message='No session found.')


@app.route('/clear_session')
def clear_session():
    session.clear()
    return render_template(template_name_or_list='session.html', message='Session cleared.')    



@app.route('/set_cookie')
def set_cookie():
    response = make_response(render_template('session.html', message='Cookie has been set!'))
    response.set_cookie('cookie_name', 'cookie_value')
    return response


@app.route('/get_cookie')
def get_cookie():
    cookie_value=request.cookies.get('cookie_name')
    return make_response(render_template('session.html', message=f'Cookie Value: {cookie_value}'))


@app.route('/clear_cookie')
def clear_cookie():
    response = make_response(render_template('session.html', message='Cookie removed'))
    response.set_cookie('cookie_name', expires=0)
    return response
    
if __name__ in "__main__":
    app.run(debug=True)