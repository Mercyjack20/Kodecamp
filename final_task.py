from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

DATABASE_URL = "sqlite:///./portfolio.db"

engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
DB_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Database Models
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    link = Column(String)

class BlogPost(Base):
    __tablename__ = "blogposts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    message = Column(Text)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Pydantic Models
class ProjectCreate(BaseModel):
    title: str
    description: str
    link: str

class ProjectUpdate(BaseModel):
    title: str
    description: str
    link: str

class BlogPostCreate(BaseModel):
    title: str
    content: str

class BlogPostUpdate(BaseModel):
    title: str
    content: str

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str
    

# Dependency to get DB session
def get_db():
    db = DB_session()
    try:
        yield db
    finally:
        db.close()
        
# Project Endpoints
@app.post("/projects/", response_model=ProjectCreate)
def create_project(project: ProjectCreate, db: session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/", response_model=list[ProjectCreate])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@app.get("/projects/{project_id}", response_model=ProjectCreate)
def get_project(project_id: int, db: session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectCreate)
def update_project(project_id: int, project: ProjectUpdate, db: session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.delete("/projects/{project_id}", response_model=ProjectCreate)
def delete_project(project_id: int, db: session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project

'''
PROJECTS
**Post** '/projects' - Add a new project
**Get** '/projects' - Get all projects
**Get** '/projects/<project_id>' - Get a single project
**Put** '/projects/<project_id>' - Update a project
**Delete** '/projects/<project_id>' - Delete a project

'''
  
# Blog Post Endpoints
@app.post("/blogposts/", response_model=BlogPostCreate)
def create_blogpost(blogpost: BlogPostCreate, db: session = Depends(get_db)):
    db_blogpost = BlogPost(**blogpost.dict())
    db.add(db_blogpost)
    db.commit()
    db.refresh(db_blogpost)
    return db_blogpost

@app.get("/blogposts/", response_model=list[BlogPostCreate])
def get_blogposts(db: session = Depends(get_db)):
    return db.query(BlogPost).all()

@app.get("/blogposts/{blogpost_id}", response_model=BlogPostCreate)
def get_blogpost(blogpost_id: int, db: session = Depends(get_db)):
    blogpost = db.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if blogpost is None:
        raise HTTPException(status_code=404, detail="Blog Post not found")
    return blogpost

@app.put("/blogposts/{blogpost_id}", response_model=BlogPostCreate)
def update_blogpost(blogpost_id: int, blogpost: BlogPostUpdate, db: session = Depends(get_db)):
    db_blogpost = db.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if db_blogpost is None:
        raise HTTPException(status_code=404, detail="Blog Post not found")
    for key, value in blogpost.dict().items():
        setattr(db_blogpost, key, value)
    db.commit()
    db.refresh(db_blogpost)
    return db_blogpost

@app.delete("/blogposts/{blogpost_id}", response_model=BlogPostCreate)
def delete_blogpost(blogpost_id: int, db: session = Depends(get_db)):
    db_blogpost = db.query(BlogPost).filter(BlogPost.id == blogpost_id).first()
    if db_blogpost is None:
        raise HTTPException(status_code=404, detail="Blog Post not found")
    db.delete(db_blogpost)
    db.commit()
    return db_blogpost
    
'''
BLOGPOST
**Post** '/blog_post' - Add a new blogpost
**Get** '/blog_post' - Get all blogposts
**Get** '/blogposts/<blogpost_id>' - Get a single blogpost
**Put** '/blogposts/<blogpost_id>' - Update a blogpost
**Delete** '/blogposts/<blogpost_id>' - Delete a blogpost

'''
    
    
# Contact Information Endpoints
@app.post("/contacts/", response_model=ContactCreate)
def create_contact(contact: ContactCreate, db: session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.put("/contacts/{contact_id}", response_model=ContactCreate)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=ContactCreate)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact
    
'''
CONTACT INFORMATION
**Post** '/contacts' - Add contact information
**Put** '/contacts/<contact_id>' - Update a contact information
**Delete** '/contacts/<contact_id>' - Delete a contact information

'''