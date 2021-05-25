from flask import Flask,redirect, render_template,session,request,abort,json,url_for

from pymongo import MongoClient
import os
import secrets
from werkzeug.utils import secure_filename
from auth import auth as auth_blueprint
from models.utils import *

from bson.objectid import ObjectId
app=Flask(__name__)

secret_key=secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = secret_key
app.register_blueprint(auth_blueprint)


user=[]

#db=MongoClient("mongodb://localhost:27017/").projects.users
UPLOAD_FOLDER = './static/img/bgImage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route("/")
@app.route("/<string:name>")
def main(name=None):
    #print(current_user)
    print(name)
    if not session.get("user"):
        if(name==None):
            return redirect(url_for('auth.login'))

        usuario=json.loads(getUser(name))
     
        return render_template('index.html',user=usuario)
    
    
    return render_template('index.html',user=session['user'])

@app.route('/project/<int:id>/edit', methods=('GET','POST'))
def editproject(id):
    id=getProjectId(id)
    #project=user['projects'][id]
    project=session['user']['projects'][id]
    if(id>-1):
    
        if request.method == 'POST':
            
            name=request.form['inputname']
            proj=user['projects'][id]
            img=request.files['inputimg']
            caminho=proj['img']
            link=request.form['inputlink']
            project={'id':project['id'],'name':name,'img':caminho,'link':link}
            usuario=session['user']
            usuario['projects'][id]=project
            
            if(img.filename!=""):
                try:
                    caminho=salvarArquivos(img)
                    os.remove(proj['img'])
                except OSError as e:
                    print(f"Error:{ e.strerror}")
            
            with MongoClient() as conn:
                db=conn.projects.users
            
                db.find_one_and_update(
                    {'name':usuario['name']},
                    {"$set":usuario},
                    upsert=True
                )
                session['user']=usuario
                return redirect(url_for('main'))
            
    
    
    #return render_template('learning.html',user=user)
    return render_template('editproject.html',project=project)
@app.route("/project/add",methods=['POST','GET'])
def addProject():
    #print(request.form)
    if request.method == 'POST':
        id=GerarId()  
        name=request.form['inputname']
        img=request.files['inputimg']
        caminho=salvarArquivos(img)
        
        link=request.form['inputlink']
        project={'id':id,'name':name,'img':caminho,'link':link}
        #projects=user['projects']
        usuario=session['user']
        projects=usuario['projects']
        projects.append(project)
        usuario['projects']=projects
        #user['projects']=projects
        
        with MongoClient() as conn:
            db=conn.projects.users
           
            db.find_one_and_update(
                {'name':usuario['name']},
                {"$set":usuario},
                upsert=True
            )
            session['user']=usuario
    
        
    return redirect(url_for('main'))

@app.route("/project/<int:id>/delete",methods=['POST'])
def deleteProject(id):
    

        
    id=getProjectId(id)
    #project=user['projects'][id]
    usuario=session['user']
    project=usuario['projects'][id]
    try:
        os.remove(project['img'])
    except OSError as e:
        print(f"Error:{ e.strerror}")
    
    #user['projects'].remove(project)
    usuario['projects'].remove(project)   
        
    with MongoClient() as conn:
        db=conn.projects.users
           
        db.find_one_and_update(
                 {'name':usuario['name']},
                    {"$set":usuario},
                    upsert=True
            )
        session['user']=usuario   
    
        
    return redirect(url_for('main'))

@app.route("/project")
def project():
    if not session.get("user"):
        return redirect(url_for('auth.login'))

    return render_template('project.html',user=session['user'])

@app.route("/learn/add",methods=['POST','GET'])
def addLearn():
    #print(request.form)
   
    if request.method == 'POST':
        
        id=GerarId()
        name=request.form['inputname']
        #img=request.form['inputimg']
        img=request.files['inputimg']
        caminho=salvarArquivos(img)

        icon=request.form['inputicon']
        link=request.form['inputlink']
        tutorial={'id':id,'name':name,'img':caminho,'icon':icon,'link':link}
        usuario=session['user']
        #tutoriais=user['tutoriais']
        tutoriais=usuario['tutoriais']
        tutoriais.append(tutorial)
        usuario['tutoriais']=tutoriais
        #user['tutoriais']=tutoriais
        #salvarImg(request.form['inputimg'])
        with MongoClient() as conn:
            db=conn.projects.users
           
            db.find_one_and_update(
                {'name':usuario['name']},
                {"$set":usuario},
                upsert=True
            )
            session['user']=usuario
    
        
    return redirect(url_for('main'))



@app.route('/learn/<int:id>/edit', methods=('GET','POST'))
def editlearn(id):
    id=getLearnId(id)
    usuario=session['user']
    #tutorial=user['tutoriais'][id]
    tutorial=usuario['tutoriais'][id]
    if(id>-1):
  
    
        if request.method == 'POST':
            
            name=request.form['inputname']
            
            tut=usuario['tutoriais'][id]
            #tut=user['tutoriais'][id]
            img=request.files['inputimg']
            caminho=tut['img']
            
            if(img.filename!=""):
                
                try:
                    caminho=salvarArquivos(img)
                    os.remove(tut['img'])
                except OSError as e:
                    print(f"Error:{ e.strerror}")
            icon=request.form['inputicon']
            link=request.form['inputlink']
            tutorial={'id':tutorial['id'],'name':name,'img':caminho,'icon':icon,'link':link}
            #user['tutoriais'][id]=tutorial
            usuario['tutoriais'][id]=tutorial
           
    
            #user['tutoriais'].remove(tutorial)
            
            with MongoClient() as conn:

                db=conn.projects.users
            
                db.find_one_and_update(
                    {'name':usuario['name']},
                    {"$set":usuario},
                    upsert=True
                )
                session['user']=usuario
                return redirect(url_for('main'))
            
    
    
    #return render_template('learning.html',user=user)
    return render_template('editlearn.html',tuto=tutorial)

@app.route("/learn/<int:id>/delete",methods=['POST'])
def deleteLearn(id):    
        
    id=getLearnId(id)
    usuario=session['user']
    tutorial=usuario['tutoriais'][id]
    #tutorial=user['tutoriais'][id]
    try:
        os.remove(tutorial['img'])
    except OSError as e:
        print(f"Error:{ e.strerror}")

    usuario['tutoriais'].remove(tutorial)
    #user['tutoriais'].remove(tutorial)
        
    with MongoClient() as conn:
        db=conn.projects.users
           
        db.find_one_and_update(
                 {'name':usuario['name']},
                    {"$set":usuario},
                    upsert=True
            )
        session['user']=usuario
    
        
    return redirect(url_for('main'))



@app.route("/learn/")
def learningPage():
    if not session.get("user"):
        return redirect(url_for('auth.login'))

    dados=CarregarAreas()
    return render_template('learning.html',user=session['user'],campos=dados)



@app.route("/get")
def getUsers():
    try:
        
        data=[]
        with MongoClient() as conn:
            db=conn.projects.users
            #data= [a for a in db.find({},{"_id":False})]
            
            data=[a for a in db.find({},{"_id":False})]
            #print(data)
            #return data
            return json.dumps(data, ensure_ascii=False).encode('utf8')
       
        return "não foi possivel se conectar ao servidor"

    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/getuser/<id>")
def getUserById(id):
    #print(id)
    
    try:
        print("entrou")
        data=[]
        with MongoClient() as conn:
            db=conn.projects.users
        
            data=[i for i in db.find({"_id": ObjectId(id)},{"_id":False})]
            #data=  [a for a in db.find_one({"_id":ObjectId ("60a4403c6de38bb253caf9b2")},{"_id":False})]
            #data=[a for a in db.find({"name":name})]
            #
            #print(data)
            return json.dumps(data, ensure_ascii=False).encode('utf8')
            #return data
       
        return  "não foi possivel se conectar ao servidor"

    except Exception as e:
        return json.dumps({'error':str(e)})



@app.route("/get/<string:name>")
def getUser(name=None):
    try:
        
        data=[]
        with MongoClient() as conn:
            db=conn.projects.users
            data=   db.find_one({"name":name},{"_id":False})
            #data=[a for a in db.find({"name":name})]
            #
            return json.dumps(data, ensure_ascii=False).encode('utf8')
            #return data
       
        return  "não foi possivel se conectar ao servidor"

    except Exception as e:
        return json.dumps({'error':str(e)})

def getProject(name):
    projects=session['user']['projects']
    #projects=user['projects']
    names=[a['name'] for a in projects]
    
    return names.index(name)
def getProjectId(id):
    projects=session['user']['projects']
    #projects=user['projects']
    ids=[int(a['id']) for a in projects]
    return ids.index(id)

def getLearn(name):
    tutoriais=session['user']['tutoriais']
    #tutoriais=user['tutoriais']
    names=[a['name'] for a in tutoriais]
    
    return names.index(name)
def getLearnId(id):
    tutoriais=session['user']['tutoriais']
    #tutoriais=user['tutoriais']
    
    ids=[int(a['id']) for a in tutoriais]
    #print(ids)
    return ids.index(id)



def salvarArquivos(arq):
    
    complemento=GerarId()
    
    
    campo=app.config['UPLOAD_FOLDER']+"/"+(secure_filename(complemento+".jpg"))
    arq.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(complemento+".jpg")))
    #print(campo)
    return campo
   
if __name__=="__main__":
    
    #user=getUser("Pedro Victor")  
    #user=json.loads(user)
    app.run(port=80)
   
    
   

