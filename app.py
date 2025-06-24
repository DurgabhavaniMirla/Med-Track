from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('user_type') or 'patient'  # role should match the form's select name

        if role == 'doctor':
            session['user'] = {
                'name': 'Dr. John',
                'email': email,
                'specialization': 'Cardiology',
                'experience': '8 years'
            }
            session['role'] = 'doctor'
            return redirect(url_for('doctor_dashboard'))
        else:
            session['user'] = {
                'name': 'John Doe',
                'email': email,
                'gender': 'Male',
                'age': 28
            }
            session['role'] = 'patient'
            return redirect(url_for('patient_dashboard'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Normally you would save this to a DB
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')
        role = request.form.get('user_type')

        session['user'] = {
            'name': name,
            'email': email,
            'gender': gender,
            'age': age
        }
        session['role'] = role

        if role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        else:
            return redirect(url_for('patient_dashboard'))

    return render_template('signup.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    user = session.get('user')
    role = session.get('role')

    if not user or role != 'patient':
        return redirect(url_for('login'))

    if request.method == 'POST':
        specialization = request.form['specialization']
        date = request.form['date']
        time = request.form['time']
        symptoms = request.form['symptoms']
        print("Appointment Booked:", specialization, date, time, symptoms)
        return redirect(url_for('patient_dashboard'))

    return render_template('appointment.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    user = session.get('user')
    role = session.get('role')
    if not user or role != 'patient':
        return redirect(url_for('login'))

    appointments = [
        {"doctor": "Dr. Smith", "date": "2025-06-28", "time": "10:00 AM", "status": "Confirmed"},
        {"doctor": "Dr. Patel", "date": "2025-06-22", "time": "3:00 PM", "status": "Completed"},
    ]

    return render_template('patient_dashboard.html', user=user, appointments=appointments)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    user = session.get('user')
    role = session.get('role')
    if not user or role != 'doctor':
        return redirect(url_for('login'))

    appointments = [
        {"patient_name": "Alice", "date": "2025-06-25", "time": "10:00 AM", "symptoms": "Fever"},
        {"patient_name": "Bob", "date": "2025-06-26", "time": "2:00 PM", "symptoms": "Cough"},
    ]

    return render_template('doctor_dashboard.html', user=user, appointments=appointments)

@app.route('/patient_details')
def patient_details():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('patient_details.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
