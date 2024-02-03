from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from . models import Users, Requisites, PaymentRequests, db
from werkzeug.security import generate_password_hash



@app.route('/', methods=['POST', 'GET'])
def index():
    requisites_query = db.session.query(Requisites).order_by(Requisites.id)
    return render_template('index.html', requisites=requisites_query)


@app.route('/sort', methods=['POST'])
def sort():
    column = request.form['column']
    order = request.form['order']
    
    if order == 'asc':
        requisites = db.session.query(Requisites).order_by(getattr(Requisites, column).asc()).all()
    else:
        requisites = db.session.query(Requisites).order_by(getattr(Requisites, column).desc()).all()

    requisites_data = [{'id': r.id, 'payment_type': r.payment_type, 'account_type': r.account_type, 'owner_name': r.owner_name, 'phone_number': r.phone_number, 'limit': str(r.limit), 'account': r.account} for r in requisites]
    return jsonify(requisites=requisites_data)


@app.route('/search', methods=['POST'])
def search():
    column = request.form['column']
    search_term = request.form['searchTerm']
    order = request.form.get('order', 'asc')

    if column == 'id' and search_term.isdigit():
        search_term = int(search_term)
        requisites = db.session.query(Requisites).filter(Requisites.id == search_term).all()
    elif column == 'id' and not search_term.strip():
        requisites = db.session.query(Requisites).order_by(getattr(Requisites, column).asc() if order == 'asc' else getattr(Requisites, column).desc()).all()            
    elif column == 'payment_type':
        requisites = db.session.query(Requisites).filter(Requisites.payment_type.ilike(f'%{search_term}%')).all()
    elif column == 'account_type':
        requisites = db.session.query(Requisites).filter(Requisites.account_type.ilike(f'%{search_term}%')).all()
    elif column == 'owner_name':
        requisites = db.session.query(Requisites).filter(Requisites.owner_name.ilike(f'%{search_term}%')).all()
    elif column == 'phone_number':
        requisites = db.session.query(Requisites).filter(Requisites.phone_number.ilike(f'%{search_term}%')).all()
    elif column == 'limit':
        search_term = float(search_term)
        requisites = db.session.query(Requisites).filter(Requisites.limit.ilike(f'%{search_term}%')).all()
    elif column == 'account':
        requisites = db.session.query(Requisites).filter(Requisites.account.ilike(f'%{search_term}%')).all()
    else:
        requisites = db.session.query(Requisites).order_by(getattr(Requisites, column).asc()).all()

    requisites_data = [{'id': r.id, 'payment_type': r.payment_type, 'account_type': r.account_type, 'owner_name': r.owner_name, 'phone_number': r.phone_number, 'limit': str(r.limit), 'account': r.account} for r in requisites]
    return jsonify(requisites=requisites_data)


@app.route('/payment_requests', methods=['POST', 'GET'])
@login_required
def payment_requests():
    payment_requests_query = db.session.query(PaymentRequests).join(Requisites)
    return render_template('payment_requests.html', payment_requests = payment_requests_query)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('payment_requests'))

    if request.method == 'POST':
        user = db.session.query(Users).filter(Users.username == request.form['username']).first()
        if user and user.check_password(request.form['password']):
            rm = True if request.form.get('remaindme') else False
            login_user(user, remember=rm)
            return redirect(url_for('payment_requests'))
        flash("Invalid username/password", 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username, password, password2 = request.form['username'], request.form['password'], request.form['password2']
        check_username = db.session.query(Users).filter(Users.username == username).count()
        if check_username:
            flash('User already exists', 'error')
        elif password != password2:
            flash('Password mismatch', 'error')
        else:
            hash = generate_password_hash(request.form['password'])
            new_user = Users(username=username, password=hash)
            db.session.add(new_user)
            db.session.commit()
            flash('Successful registration', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')
