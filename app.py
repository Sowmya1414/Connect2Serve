from flask import Flask,render_template,request,url_for,flash,redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from datetime import datetime
app=Flask(__name__)


app.config['SECRET_KEY']="secret key!!!"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:hello@localhost/connect2serve_db_1'
db=SQLAlchemy(app)
migrate= Migrate(app,db)
# flask login
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    ph_no = db.Column(db.String(20), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Events', backref='user')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash , password)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Events(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_address = db.Column(db.String(300), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    event_url = db.Column(db.String(300), nullable=False)
    event_date = db.Column(db.String(10), nullable=False)
    event_time = db.Column(db.String(10), nullable=False)
    about_event= db.Column(db.Text)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form.get('user_name')
        email=request.form.get('email')
        password=request.form.get('password')
        role=request.form.get('role')
        district=request.form.get('district')
        ph_no=request.form.get('ph_no')
        user=Users.query.filter_by(username=username).first()
       
        if user is None:
            hashed=generate_password_hash(password,"sha256")
            data= Users(username=username,email=email,password_hash=hashed,role=role,district=district,ph_no=ph_no)
            db.session.add(data)
            db.session.commit()
            #  flash('Account created successfully')
            return redirect(url_for('home'))

        else:
            #  flash('There is some error. Try again...')
            return render_template('home')
            

    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('user_name')
        password=request.form.get('password')
        user=Users.query.filter_by(username=username).first()
        if user :
            if  check_password_hash(user.password_hash,password):
                login_user(user)
                # flash('Logged in !')
                if user.role=='organizer':
                    return render_template('org_base.html')
                else:
                    return render_template('vol_base.html')
            else:
                # flash('worng password')
                return redirect(url_for('home'))
        else:
            # flash("user doesn't exist!")
            return redirect(url_for('home'))
    return redirect(url_for('home'))




if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)