from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from models.tables import Item
from models.forms import RegisterForm

app =  Flask(__name__)

app.config['DEBUG'] = True

user, password = 'NJgaliza', 'doritos'
host = 'NJgaliza.mysql.pythonanywhere-services.com'
db = 'NJgaliza$tecfun'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(user, password, host, db)
db = SQLAlchemy(app)

#app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.username

all_users = {
    "admin": User("admin", generate_password_hash("secret")),
    "test": User("test", generate_password_hash("test")),
}

app.secret_key = 'Henshin'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')



@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("login.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login.html", error=True)

    login_user(user)
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form =  RegisterForm()
    if form.validate_on_submit():
        i = Item(
            name = form.name.data
            )
        db.session.add(i)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('create.html', form=form)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = RegisterForm()
    item = Item.query.filter_by(_id=id).first()

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()

    form = RegisterForm()
    form.insert_data(item)
    return render_template('update.html', form=form)

@app.route('/read')
def read():
    itens = Item.query.all()
    return render_template('read.html',itens=itens)

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.filter_by('_id=id').first()

    db.sesion.delete(item)
    db.session.commit()
    return redirect(url_for('main'))














