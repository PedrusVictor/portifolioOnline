from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,id,name,desc,cursos,skills,projects,tutoriais):
        self.id=id
        self.name=name
        self.desc=desc
        self.cursos=cursos
        self.skills=skills
        self.projects=projects
        self.tutoriais=tutoriais
    
  