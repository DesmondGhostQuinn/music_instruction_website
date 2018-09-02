from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
#from flask.ext.pymongo import PyMongo
import bcrypt

app = Flask(__name__)

#app.url_map.strict_slashes = False  

app.config['MONGO_DBNAME'] = 'connect_to_mongo'
app.config['MONGO_URI'] = 'mongodb://test:sainasimran1@ds129321.mlab.com:29321/connect_to_mongo'
#app.config['MONGO_URI'] = 'mongodb://users:sainasimran1@ds129321.mlab.com:29321/connect_to_mongo'

client = MongoClient('MONGO_URI') 
db=client.connect_to_mongo
collection = db['users'] #just added

mongo = PyMongo(app)


@app.route('/')

#def homepage():                
    #render_template('index.html')                #just added

def index():
	if 'username' in session:
		#return 'You are logged in as ' + session['username']
		#return render_template('profile.html',username= session['username'])      
		#return render_template('profile2.html',password="password")
		#password=db.users.find({},{"password":1})
		#password = mongo.db.users.find_one_or_404({"password": True})
		password = mongo.db.users.find_one({'name': session['username']})
		return render_template('profile2.html',username=password['name'],password=password['password'],instrument=password['instrument'], coursed=password['coursed'], course=password['course'])		#just added

	return render_template('homepage.html')  




@app.route('/login', methods=['POST', 'GET'])
def login():
    #return redirect(url_for('login1'))  
    #return render_template('login.html')          
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            #if (request.form['pass'], login_user['password']) == login_user['password']:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
              
                session['username'] = request.form['username']
                return redirect(url_for('index'))        
                #return render_template('homepage.html')

    
        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())   
            #users.insert({'name' : request.form['username'], 'password' : hashpass})
            users.insert({'name' : request.form['username'], 'password' : hashpass, 'instrument' : request.form['instrument'],'coursed' : request.form['coursed'],'course' : request.form['course']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('signup.html')

@app.route('/aboutpage', methods=['GET'])
def aboutpage():
    return render_template('aboutpage.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
