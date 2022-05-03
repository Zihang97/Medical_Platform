from flask import Flask, request, redirect, url_for, render_template
import json
import Modules.device_module as device_module
import Modules.chat_module as chat_module
import Modules.user as user
import Modules.role as role
import Modules.mp_assignment as mp_assignment
import Modules.calendar_module as calendar

app = Flask(__name__)


# this is the index page which everyone can visit. There are login and register options provided in this page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        dob = request.form['dob']
        pwd = request.form['password']
        repwd = request.form['repassword']
        users = user.get_users_password()
        if not username:
            return 'Empty Username!'
        if not pwd:
            return 'Empty Password!'
        if pwd == repwd:
            if username in users:
                return 'User Already Exist'
            else:
                user.insert_user(username, pwd, email, age, gender, dob)
                role.add_role(username, 'None')
                return redirect(url_for('login'))
            # user will be redirect to index page after register.
        else:
            return 'password should be identical to repassword'
    return render_template('register.html')


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        users = user.get_users_password()
        if username in users:
            if pwd == users[username]:
                return redirect(url_for('jump', name=username))
            else:
                return render_template('login_return.html', text='Wrong Password!')
        else:
            return render_template('login_return.html', text='Username Not Found, please register first!')
    return render_template('login.html')


# check if we have user in our list, if we do, user log in successfully.
# else, user either does not register or enters wrong password


@app.route('/jump/<name>', methods=['GET', 'POST'])
def jump(name):
    user_roles = role.get_roles()
    if 'Admin' in user_roles[name]:
        return redirect(url_for('admin', name=name))
    elif 'Patient' in user_roles[name]:
        return redirect(url_for('patient', name=name))
    else:
        return redirect(url_for('mp', name=name))


# this is the main page for patient logging in successfully
@app.route('/patient/<name>', methods=['GET', 'POST'])
def patient(name):
    doctors, nurses = mp_assignment.get_one_assignment(name)
    return render_template('patient.html', name=name, doctors=' '.join(doctors), nurses=' '.join(nurses))


# this is the main page for MP logging in successfully
@app.route('/MP/<name>', methods=['GET', 'POST'])
def mp(name):
    patients = mp_assignment.get_patients(name)
    patients_results = []
    appoint_results = []
    for patient in patients:
        temp_dic = {'PatientName': patient, 'Temperature': 'None',
                    'BloodPressure': 'None', 'Pulse': 'None',
                    'Oximeter': 'None', 'Weight': 'None',
                    'Height': 'None', 'Glucometer': 'None'}
        results = device_module.get_device(patient)
        for result in results:
            temp_dic[result[1]] = result[2]
        patients_results.append(temp_dic)

        appointments = calendar.get_appointment(name)
        for appointment in appointments:
            appoint_dic = {'PatientName': appointment[2], 'Appointment date': appointment[3],
                           'Symptoms': appointment[6], 'Start time': appointment[4], 'End time': appointment[5]}
            appoint_results.append(appoint_dic)

    return render_template('MP.html', name=name, patients_results=patients_results, appointment_resutls = appoint_results)


# this is the main page for MP logging in successfully
@app.route('/device/<name>', methods=['GET', 'POST'])
def device(name):
    if request.method == 'POST':
        patientname = request.form['patientname']
        temperature = request.form['temperature']
        bloodpressure = request.form['bloodpressure']
        pulse = request.form['pulse']
        oximeter = request.form['oximeter']
        weight = request.form['weight']
        height = request.form['height']
        glucometer = request.form['glucometer']
        device_dict = {'Temperature': temperature, 'BloodPressure': bloodpressure,
                       'Pulse': pulse, 'Oximeter': oximeter, 'Weight': weight,
                       'Height': height, 'Glucometer': glucometer}
        cnt = 0
        if not patientname:
            return "Patient name can't be empty!"
        for type, measurement in device_dict.items():
            if measurement:
                cnt = 1
                try:
                    temp = float(measurement)
                except:
                    return "Measurement data should be numbers!"
                if temp < 0:
                    return "Measurement data should be positive!"
                device_module.delete_device(patientname, type)
                device_module.insert_device(patientname, type, measurement)
        if cnt == 0:
            return "Measurement data can't be empty!"
    return render_template('device.html', name=name)


# this is the main page for admin logging in successfully
@app.route('/admin/<name>', methods=['GET', 'POST'])
def admin(name):
    if request.method == 'POST':
        username = request.form['username']
        new_role = request.form['new_role']
        user_roles = role.get_roles()
        users = user.get_users_password()
        if username not in users:
            return 'User Not Exist!'
        if username in user_roles and new_role in user_roles[username]:
            return 'Role Already Exists!'
        role.add_role(username, new_role)
    user_roles = role.get_roles()
    patients = set()
    patients_assigned = set()
    for username, roles in user_roles.items():
        if 'Patient' in roles:
            patients.add(username)
    assign_results = mp_assignment.get_all_assignments()
    for assign_result in assign_results:
        patients_assigned.add(assign_result[0])
    patients_unassigned = patients - patients_assigned
    return render_template('admin.html', name=name, user_roles=user_roles,
                           assign_results=assign_results, patients_unassigned=patients_unassigned)


@app.route('/admin/update/<name>/<username>/<ori_role>', methods=['POST'])
def admin_update_role(name, username, ori_role):
    if request.method == 'POST':
        new_role = request.form['new_role']
        user_roles = role.get_roles()
        if new_role in user_roles[username]:
            return 'Role Already Exists!'
        role.update_role(username, ori_role, new_role)
        return redirect(url_for('admin', name=name))


@app.route('/admin/delete/<name>/<username>/<ori_role>', methods=['POST'])
def admin_delete_role(name, username, ori_role):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'delete':
            role.delete_role(username, ori_role)
        return redirect(url_for('admin', name=name))


@app.route('/admin/add/<name>', methods=['POST'])
def admin_add_assignment(name):
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        type = request.form['type']
        mp_name = request.form['mp_name']
        users = user.get_users_password()
        if patient_name not in users:
            return 'Patient Not Exist!'
        if mp_name not in users:
            return 'MP Not Exist!'
        mp_assignment.insert_assignment(patient_name, type, mp_name)
        return redirect(url_for('admin', name=name))


@app.route('/admin/delete/<name>/<username>/<type>/<mp_name>', methods=['POST'])
def admin_delete_assignment(name, username, type, mp_name):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'delete':
            mp_assignment.delete_assignment(username, type, mp_name)
        return redirect(url_for('admin', name=name))


@app.route('/chat/<name>', methods=['GET', 'POST'])
def chat(name):
    if request.method == 'POST':
        recipient = request.form['recipient']
        users = user.get_users_password()
        if recipient not in users:
            return 'Recipient Not Exist!'

        text_message = request.form['text_message']
        video = request.files['video']
        voice = request.files['voice']
        if video:
            video.save('./static/' + video.filename)
            current_time = chat_module.current_time()
            chat_module.store_message(name, recipient, 'VIDEO', '../../static/file_buffer/' + video.filename,
                                      current_time)
        if voice:
            voice.save('./static/' + voice.filename)
            current_time = chat_module.current_time()
            chat_module.store_message(name, recipient, 'VOICE', '../../static/file_buffer/' + voice.filename,
                                      current_time)
        if text_message:
            current_time = chat_module.current_time()
            chat_module.store_message(name, recipient, 'TEXT', text_message, current_time)
        if not (text_message or video or voice):
            return "Message can't be empty!"
    return redirect(url_for('jump', name=name))


@app.route('/chat/display/<name>', methods=['GET', 'POST'])
def chat_display(name):
    if request.method == 'POST':
        recipient = request.form['recipient']
        results = chat_module.get_messages(name, recipient)
        return render_template('display.html', name=name, results=results)


@app.route('/appointment/<name>', methods=['GET', 'POST'])
def make_appointment(name):
    if request.method == 'POST':
        doctor = request.form['doctor']
        date = request.form['date']
        startime = request.form['startime']
        endtime = request.form['endtime']
        symptom = request.form['symptom']
        calendar.make_appointment(doctor, name, date, startime, endtime, symptom)
    return redirect(url_for('jump', name=name))


@app.route('/appointment/display/<name>', methods=['GET', 'POST'])
def appointment_display(name):
    if request.method == 'POST':
        mp = request.form['doctor']
        doctor, nurse = mp_assignment.get_one_assignment(name)
        if not mp:
            appoints = calendar.get_appointment(name)
        elif mp in doctor or nurse:
            appoints = calendar.get_one_appointment(name, mp)
        else:
            redirect(url_for('jump', name=name))
    return render_template('appointment.html', name=name, results=appoints)


if __name__ == '__main__':
    app.run()
