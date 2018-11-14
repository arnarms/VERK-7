import bottle
from bottle import run, route, template, static_file, request, hook, redirect
from beaker.middleware import SessionMiddleware
from functools import wraps
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4

from sys import argv

Base = declarative_base()
engine = create_engine('mysql+pymysql://1505982309:ZByy2vtJ7T7Rebmr@tsuts.tskoli.is/1505982309_verk7')

app = bottle.app()
plugin = sqlalchemy.Plugin(engine, keyword='db')
app.install(plugin)
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'jhfkjshgjshgfjfdhfgenejnjvnjfnvjnjsvsljflsjfak',
    'session.httponly': True,
    'session.timeout': 3600 * 24,
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)

class user(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))


@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in request.session:
            return f(*args, **kwargs)
        else:
            redirect('/login')
    return wrap

@route('/test')
def test_db(db):
    table_data = db.query(user)
    res = []
    for x in table_data:
        res.append({'username':x.username })

    return {'table_data': res}

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
def index():
    if 'username' in request.session:
        return template('index')
    else:
        return template('index_open')


@route('/register')
def register():
    return template('register')

@route('/register', method='POST')
def do_register(db):
    name = request.forms.get('name')
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    #query to make sure no username exists
    result = db.query(user).filter(user.username==username).first()
    if result == None:
        new_user = user(name=name, username=username, password=password)
        db.add(new_user)
        db.commit()
        request.session['username'] = username
        request.session.save()
        redirect('/')
    else:
        redirect('/register')

@route('/login')
def login():
    return template('login')

@route('/login', method='POST')
def do_login(db):
    username = request.forms.get('username')
    password = request.forms.get('password')
    result = db.query(user).filter(user.username==username).first()
    if result == None:
        redirect('/login')
    if result.password == password:
        request.session['username'] = username
        request.session.save()
        redirect('/')
    else:
        redirect('/login')


@route('/admin')
@login_required
def admin():
    name = request.session['username']
    return template('admin', name=name)


@route('/logout')
def logout():
    if 'username' in request.session:
        request.session.delete()
        redirect('/')
        
bottle.run(app=app, host="0.0.0.0", port=argv[1], reloader=True, debug=True)
  