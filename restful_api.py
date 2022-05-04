from flask import Flask, request
from flask_restful import abort, Api, Resource, reqparse
import Modules.device_module as device_module
import Modules.chat_module as chat_module
import Modules.user as user
import Modules.calendar_module as calendar_module

app = Flask(__name__)
api = Api(app)

class Device(Resource):
    def get(self):
        patient = request.form['patientname']
        results = device_module.get_device(patient)
        temp_dic = {"patientname": patient}
        for result in results:
            temp_dic[result[1]] = result[2]
        return temp_dic

    def post(self):
        patientname = request.form['patientname']
        temperature = request.form['Temperature']
        systolicbloodpressure = request.form['SystolicBloodPressure']
        diastolicbloodpressure = request.form['DiastolicBloodPressure']
        pulse = request.form['Pulse']
        oximeter = request.form['Oximeter']
        glucometer = request.form['Glucometer']
        device_dict = {'Temperature': temperature, 'SystolicBloodPressure': systolicbloodpressure,
                       'DiastolicBloodPressure': diastolicbloodpressure, 'Pulse': pulse,
                       'Oximeter': oximeter, 'Glucometer': glucometer}
        cnt = 0
        if not patientname:
            abort(404, message="Patient name can't be empty!")
        for type, measurement in device_dict.items():
            if measurement:
                cnt = 1
                try:
                    temp = float(measurement)
                except:
                    abort(404, message="Measurement data should be numbers!")
                if temp < 0:
                    abort(404, message="Measurement data should be positive!")
                device_module.delete_device(patientname, type)
                device_module.insert_device(patientname, type, measurement)
        if cnt == 0:
            abort(404, message="Measurement data can't be empty!")
        return {"status": "Success"}


class Chat(Resource):
    def get(self):
        user1 = request.form['username1']
        user2 = request.form['username2']
        results = chat_module.get_messages(user1, user2)
        messages = []
        for result in results:
            temp_dic = {}
            temp_dic["sender"] = result[0]
            temp_dic["recipient"] = result[1]
            temp_dic["type"] = result[2]
            temp_dic["content"] = result[3]
            temp_dic["time"] = str(result[4])
            messages.append(temp_dic)
        return messages


    def post(self):
        sender = request.form['sender']
        recipient = request.form['recipient']
        type = request.form['type']
        message = request.form['message']
        users = user.get_users_password()
        if sender not in users:
            abort(404, message="Sender Not Exist!")
        if recipient not in users:
            abort(404, message="Recipient Not Exist!")

        if type == 'VIDEO':
            current_time = chat_module.current_time()
            chat_module.store_message(sender, recipient, 'VIDEO', message, current_time)
        elif type == 'VOICE':
            current_time = chat_module.current_time()
            chat_module.store_message(sender, recipient, 'VOICE', message, current_time)
        elif type == 'TEXT':
            current_time = chat_module.current_time()
            chat_module.store_message(sender, recipient, 'TEXT', message, current_time)
        else:
            abort(404, message="Type not Correct!")
        return {"status": "Success"}



api.add_resource(Device, '/device')
api.add_resource(Chat, '/chat')
# curl http://127.0.0.1:5000/device -d "patientname=jzh" -X GET
# curl http://127.0.0.1:5000/device -d "patientname=jzh" -d "Temperature=37" -d "SystolicBloodPressure=110" -d "DiastolicBloodP
# ressure=70" -d "Pulse=96" -d "Oximeter=97" -d "Glucometer=83" -X POST

# curl http://127.0.0.1:5000/chat -d "username1=jzh" -d "username2=mandy" -X GET
# curl http://127.0.0.1:5000/chat -d "sender=jzh" -d "recipient=mandy" -d "type=TEXT" -d "message=good everning mandy" -X POST


if __name__ == '__main__':
    app.run(debug=True)