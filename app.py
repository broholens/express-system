"""
TODO:
1. 数据库密码从env中获取
"""
import os
import secrets
import functools

from flask import Flask, request, make_response, jsonify, current_app
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, AnonymousUserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug import secure_filename, generate_password_hash, check_password_hash
from flask_cors import CORS

from config import EXPRESS_PRICE_HEADER, UPLOAD_FOLDER, INIT_DB_SQL


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Changeme_123@localhost:3306'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)
db = SQLAlchemy(app)
db.session.execute(INIT_DB_SQL)
db.session.commit()


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    discount = db.Column(db.Float, default=1.00)

    @staticmethod
    def init_roles():
        roles = {
            'Gold': 1.00,
            'Platinum': 0.95,
            'Diamond': 0.90,
            'Administrator': 1.00,
        }
        for name, discount in roles.items():
            db.session.add(Role(name=name, discount=discount))
        db.session.commit()

    @staticmethod
    def set_discount(name, discount):
        role = Role.query.filter(Role.name == name).first()
        if not role:
            db.session.add(Role(name=name, discount=discount))
        else:
            role.discount = discount
        db.session.commit()

class Customer(db.Model, UserMixin):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # 注册成为黄金会员
    role = db.Column(db.String(64), default='Gold')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'token': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('token') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = Customer.query.get(data.get('token'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def register(username, password):
        user = db.session.query(Customer.username == username).first()
        if user:
            return False
        password_hash = generate_password_hash(password)
        db.session.add(Customer(username=username, password_hash=password_hash))
        db.session.commit()
        return True

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

class ExpressPrice(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_ = db.Column(db.String(16), nullable=False, index=True)
    to_ = db.Column(db.String(16), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    price_formula = db.Column(db.String(40), default='X')
    remarks = db.Column(db.Text)

def admin_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'Administrator':
            return 'Permission denied', 401
        return func(*args, **kwargs)
    return wrapper

def load_excel_rows(file_path):
    import pandas
    data = pandas.read_excel(file_path, names=EXPRESS_PRICE_HEADER)
    for _, row in data.iterrows():
        yield row

def _import_express_price(file_path):
    for row in load_excel_rows(file_path):
        data = ExpressPrice.query.filter(
            ExpressPrice.from_ == row['from_'],
            ExpressPrice.to_ == row['to_'],
            ExpressPrice.name == row['name']
        ).first()
        if not data:
            db.session.add(ExpressPrice(**row))
    db.session.commit()

# @admin_required
@app.route('/import-express-price', methods=['POST'])
def import_express_price():
    express_price_file = request.files.get('file')
    if not express_price_file:
        return make_response('No file found.', 400)
    filename = secure_filename(express_price_file.filename)
    tmp_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    express_price_file.save(tmp_file)
    _import_express_price(tmp_file)
    return make_response('Import express success.', 200)

# @login_required
@app.route('/query', methods=['POST'])
def query():
    from_ = request.form.get('from_')
    to_ = request.form.get('to_')
    weight = float(request.form.get('weight'))
    data_set = ExpressPrice.query.filter(ExpressPrice.from_ == from_, ExpressPrice.to_ == to_).all()
    result = []
    for data in data_set:
        price_formula = data.price_formula.replace('X', str(weight))
        total_price = round(eval(price_formula), 2)
        price = round(total_price / weight, 2)
        result.append({
            'name': data.name,
            'from_': data.from_,
            'to_': data.to_,
            'weight': weight,
            'price_formula': price_formula,
            'price': price,
            'currency': 'RMB',
            'total_price': total_price,
            'remarks': data.remarks
        })
    return jsonify({'expressList': result})

# @login_required
@app.route('/countries', methods=['GET'])
def get_countries():
    data_set = db.session.query(ExpressPrice.from_, ExpressPrice.to_).all()
    result = []
    for data in data_set:
        result.extend(data)
    result = [
        {'value': data}
        for data in set(result)
    ]
    return jsonify({'countries': result})

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Customer.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        login_user(user)
        g.current_user = user
        token = user.generate_token()
        return jsonify({'token': token})
    return 'Username or password is incorrect.', 401

@login_required
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()

@admin_required
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not Customer().register(username=username, password=password):
        return 'Username has been used', 400
    user = Customer.query.filter_by(username=username).first()
    login_user(user, remember=True)
    token = user.generate_token()
    return jsonify({'token': token})


if __name__ == '__main__':
    db.create_all()
    # Role().init_roles()
    app.run()
