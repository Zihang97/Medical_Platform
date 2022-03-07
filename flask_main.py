from flask import Flask, escape, request, redirect, url_for, render_template
import json
import device_module
import chat_module
import user


app = Flask(__name__)

# this is the index page which everyone can visit. There are login and register options provided in this page
@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')


# register page
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method =='POST':   
		username = request.form['username']  
		pwd = request.form['password']
		repwd = request.form['repassword']
		users = user.getusers()
		if not username:
			return 'Empty Username!'
		if not pwd:
			return 'Empty Password!'
		if pwd == repwd:
			if username in users:
				return 'User Already Exist'
			else:
				user.insertuser(username, pwd)
				chat_module.create_table(username)
				# after register userinformation is saved in user list as a dictionary
				return redirect('/')
				# user will be redirect to index page after register.
		else:
		  return('password should be identical to repassword')
	return render_template('register.html')


# login page
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method =='POST': 
		username = request.form['username']
		pwd = request.form['password']
		users = user.getusers()
		if username in users:
			if pwd == users[username]:
				return redirect(url_for('main', name = username))
			else:
				return render_template('login_return.html', text = 'Wrong Password!')
		else:
			return render_template('login_return.html', text = 'Username Not Found, please register first!')
	return render_template('login.html')
    # check if we have user in our list, if we do, user log in successfully.
    # else, user either does not register or enters wrong password



# this is the main page for user logging in successfully
@app.route('/main/<name>', methods=['GET','POST'])
def main(name):
	if request.method =='POST': 
		patientid = request.form['patientid']
		temperature = request.form['temperature']
		bloodpressure = request.form['bloodpressure']
		pulse = request.form['pulse']
		oximeter = request.form['oximeter']
		weight = request.form['weight']
		height = request.form['height']
		glucometer= request.form['glucometer']
		device_dict = {'patientid': patientid, 'temperature': temperature,
						'bloodpressure': bloodpressure, 'pulse': pulse,
						'oximeter': oximeter, 'weight': weight,
						'height': height, 'glucometer': glucometer}
		device_json = json.dumps(device_dict)
		try:
			device_module.DM(device_json, 'example.json')
		except ValueError as e:
			return e.args[0]
		except AttributeError as e:
			return e.args[0]
	return render_template('main.html', name = name)


@app.route('/chat/<name>', methods = ['GET', 'POST'])
def chat(name):
	if request.method == 'POST':
		recipient = request.form['recipient']
		users = user.getusers()
		if recipient not in users:
			return 'Recipient Not Exist!'

		text_message = request.form['text_message']
		video = request.files['video']
		voice = request.files['voice']
		if text_message:
			current_time = chat_module.current_time()
			chat_module.store_message(name, recipient, 'TEXT', text_message, 'Sent', current_time)
			chat_module.store_message(recipient, name, 'TEXT', text_message, 'Received', current_time)
		elif video:
			video.save('./static/' + video.filename)
			current_time = chat_module.current_time()
			chat_module.store_message(name, recipient, 'VIDEO', '../../static/' + video.filename, 'Sent', current_time)
			chat_module.store_message(recipient, name, 'VIDEO', '../../static/' + video.filename, 'Received', current_time)
		elif voice:
			voice.save('./static/' + voice.filename)
			current_time = chat_module.current_time()
			chat_module.store_message(name, recipient, 'VOICE', '../../static/' + voice.filename, 'Sent', current_time)
			chat_module.store_message(recipient, name, 'VOICE', '../../static/' + voice.filename, 'Received', current_time)
		else:
			return "Message can't be empty!"
	return redirect(url_for('main', name = name))


@app.route('/chat/display/<name>', methods = ['GET', 'POST'])
def chat_display(name):
	if request.method == 'POST':
		recipient = request.form['recipient']
		results = chat_module.get_messages(name, recipient)

	return render_template('display.html', name=name, results=results)

if __name__ == '__main__':
	app.run()