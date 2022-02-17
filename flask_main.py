from flask import Flask, escape, request, redirect, url_for, render_template
import json
from DeviceModule import *

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
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
			DM(device_json, 'example.json')
		except ValueError as e:
			return e.args[0]
		except AttributeError as e:
			return e.args[0]
	return render_template('index.html')

if __name__ == '__main__':
	app.run()