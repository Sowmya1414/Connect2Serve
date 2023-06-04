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
            return render_template('home.html')
            

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
                return render_template('home.html')
                
            else:
                # flash('worng password')
                return redirect(url_for('home'))
        else:
            # flash("user doesn't exist!")
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for('home'))


@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    return render_template('dashboard.html',)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html") , 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html") , 500

if __name__=='__main__':
    app.run(debug=True)