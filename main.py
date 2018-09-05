from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_pymongo import MongoClient
#from flask.ext.pymongo import PyMongo
import bcrypt
import smtplib
import yagmail

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


def index():
	if 'username' in session:
		password = mongo.db.users.find_one({'name': session['username']})
		return render_template('profile2.html',username=password['name'],password=password['password'],instrument=password['instrument'], coursed=password['coursed'], course=password['course'])		#just added

	return render_template('homepage.html')  




@app.route('/login', methods=['POST', 'GET'])
def login():
	          
	if request.method == 'POST':
		users = mongo.db.users
		login_user = users.find_one({'name' : request.form['username']})

		if login_user:
			#if (request.form['pass'], login_user['password']) == login_user['password']:
			if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
				session['username'] = request.form['username']
				session['logged_in'] = True
				return redirect(url_for('index'))     

				


		return 'Invalid username/password combination'
	return render_template('login.html')
	
	
@app.route('/logout')
#@login_required
def logout():
    session.pop('logged_in', None)
    #flash('You were logged out.')
    return redirect(url_for('home'))	

@app.route('/home')	
def home():
	return render_template('homepage.html')
	

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

	
@app.route("/form", methods=["GET", "POST"])
def my_form():
	if request.method == 'POST':
		reply_to = request.form.get('email')
		message = request.form.get('message')
		message = reply_to+'--says that--'+message
		yag = yagmail.SMTP('ourprojectmail24@gmail.com', 'sainasimran1')	#to initialize
		yagmail.SMTP('ourprojectmail24@gmail.com').send('ourprojectmail24@gmail.com', reply_to, message)
		return redirect(url_for('index'))
		
	return render_template('contact.html')	
	
@app.route('/aboutpage', methods=['GET'])
def aboutpage():
    return render_template('homepage.html')
	
@app.route('/faq')
def faq():
	return render_template('faq.html')
	
@app.route('/teachers')
def teachers():
	return render_template('teachers.html')
	
@app.route('/ccourse')
def ccourse():
	return render_template('ccourse.html')
	
@app.route('/lcourse')
def lcourse():
	return render_template('lcourse.html')
	
@app.route('/abrsm')
def abrsm():
	return render_template('abrsm.html')
	
@app.route('/lcm')
def lcm():
	return render_template('lcm.html')
	
@app.route('/trinity')
def trinity():
	return render_template('trinity.html')
	
@app.route('/bass1')
def bass1():
	return render_template('bass1.html')
	
@app.route('/guitar1')
def guitar1():
	return render_template('guitar1.html')
	
@app.route('/piano1')
def piano1():
	return render_template('piano1.html')
	
@app.route('/sax1')
def sax1():
	return render_template('sax1.html')
	
@app.route('/violin1')
def violin1():
	return render_template('violin1.html')
	
@app.route('/drums1')
def drums1():
	return render_template('drums1.html')
	

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
