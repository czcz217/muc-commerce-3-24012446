from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import os
import io
import pandas as pd

app = Flask(__name__)
app.secret_key = 'day07_secret_key'

from services import data_service, qa_service

VALID_CREDENTIALS = {
    'student': 'day07'
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('login.html', error=None)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        session['username'] = username
        return redirect('/dashboard')
    
    return render_template('login.html', error='账号或密码错误')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    category = request.args.get('category', '全部')
    data = data_service.get_dashboard_data(category)
    
    return render_template('dashboard.html', 
                           username=session['username'],
                           category=category,
                           **data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/api/ask', methods=['POST'])
def ask():
    if 'username' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    question = request.json.get('question', '')
    answer = qa_service.answer_question(question)
    
    return jsonify({'answer': answer})

@app.route('/download')
def download():
    if 'username' not in session:
        return redirect('/')
    
    category = request.args.get('category', '全部')
    df = data_service.get_filtered_dataframe(category)
    
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    filename = f'user_data_{category}.csv'
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)