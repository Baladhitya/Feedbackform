from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production

# Simple in-memory user store for demo
users = {}
submissions = []  # Store feedback submissions
forms = []  # Store created forms

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists.')
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', submissions=submissions)

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('login'))
    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')
    rating = request.form.get('rating')
    recommend = request.form.get('recommend')
    # Log submission with username
    submissions.append({
        'username': session['username'],
        'name': name,
        'email': email,
        'feedback': feedback,
        'rating': rating,
        'recommend': recommend
    })
    return redirect(url_for('success', name=name, email=email, feedback=feedback, rating=rating, recommend=recommend))

@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name')
    email = request.args.get('email')
    feedback = request.args.get('feedback')
    rating = request.args.get('rating')
    recommend = request.args.get('recommend')
    return render_template('success.html', name=name, email=email, feedback=feedback, rating=rating, recommend=recommend)

@app.route('/create_form', methods=['GET', 'POST'])
def create_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form.get('form_title')
        questions = []
        idx = 0
        while True:
            q_text = request.form.get(f'question_{idx}_text')
            q_type = request.form.get(f'question_{idx}_type')
            q_options = request.form.get(f'question_{idx}_options')
            if not q_text or not q_type:
                break
            question = {
                'text': q_text,
                'type': q_type,
                'options': [opt.strip() for opt in q_options.split(',')] if q_options and (q_type == 'radio' or q_type == 'dropdown') else []
            }
            questions.append(question)
            idx += 1
        forms.append({
            'title': title,
            'questions': questions,
            'creator': session['username'],
            'responses': []
        })
        return redirect(url_for('list_forms'))
    return render_template('create_form.html')

@app.route('/forms')
def list_forms():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('list_forms.html', forms=forms)

@app.route('/fill_form/<int:form_id>', methods=['GET', 'POST'])
def fill_form(form_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    form = forms[form_id]
    if request.method == 'POST':
        answers = []
        for idx, q in enumerate(form['questions']):
            answers.append(request.form.get(f'q{idx}'))
        form['responses'].append({
            'username': session['username'],
            'answers': answers
        })
        return redirect(url_for('view_responses', form_id=form_id))
    return render_template('fill_form.html', form=form)

@app.route('/view_responses/<int:form_id>')
def view_responses(form_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    form = forms[form_id]
    return render_template('view_responses.html', form=form)

@app.route('/edit_form/<int:form_id>', methods=['GET', 'POST'])
def edit_form(form_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    form = forms[form_id]
    if form['creator'] != session['username']:
        return "Unauthorized", 403
    if request.method == 'POST':
        form['title'] = request.form.get('form_title')
        questions = []
        idx = 0
        while True:
            q_text = request.form.get(f'question_{idx}_text')
            q_type = request.form.get(f'question_{idx}_type')
            q_options = request.form.get(f'question_{idx}_options')
            if not q_text or not q_type:
                break
            question = {
                'text': q_text,
                'type': q_type,
                'options': [opt.strip() for opt in q_options.split(',')] if q_options and (q_type == 'radio' or q_type == 'dropdown') else []
            }
            questions.append(question)
            idx += 1
        form['questions'] = questions
        return redirect(url_for('list_forms'))
    return render_template('create_form.html', form=form, edit=True)

@app.route('/delete_form/<int:form_id>', methods=['POST'])
def delete_form(form_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    form = forms[form_id]
    if form['creator'] != session['username']:
        return "Unauthorized", 403
    forms.pop(form_id)
    return redirect(url_for('list_forms'))

# Optional: Admin route to view all submissions
@app.route('/submissions')
def view_submissions():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))
    return render_template('submissions.html', submissions=submissions)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
