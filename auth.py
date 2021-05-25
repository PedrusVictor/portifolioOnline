from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from werkzeug.security import generate_password_hash, check_password_hash

from pymongo import MongoClient

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')
@auth.route("/login",methods=["POST"])
def login_post():
    name=request.form['name']
    password=request.form['password']
    remember = True if request.form['remember'] else False
    
    with MongoClient() as con:
        db=con.projects.users
        user = db.find_one({'name':name},{"_id":False})
        
        if(user['name']!=name and user['password']!=generate_password_hash(password)):
            flash("Login ou senha incorretos")
        
            return redirect(url_for('auth.login'))
       
        session['user']=user
        

       
    return redirect(url_for('main'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')
    
@auth.route('/signup', methods=['POST'])
def signup_post():
    
    name = request.form.get('name')
    password = request.form.get('password')
    desc=request.form['bio']
    cursos=request.form['cursos']
    skills=request.form['skills']
    img=request.form['img']
    projects=[]
    tutoriais=[]
    with MongoClient() as conn:
        db=conn.projects.users
        user=db.find_one({'name':name})
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash("usuario já existe")
            return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = { "name":name, "password":generate_password_hash(password, method='sha256'),"desc":desc,"cursos":cursos,"img":img,"skills":skills,"projects":projects,"tutoriais":tutoriais}
        db.insert_one(new_user)
        
    # add the new user to the database
    

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop("user",None)
    return redirect(url_for('auth.login'))

