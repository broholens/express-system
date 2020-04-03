import os
import secrets
import functools
import platform

# if platform.platform().startswith('Windows'):
#     ALLOW_ORIGIN = 'http://localhost:8080'
#     MYSQL_PWD = 'Changeme_123'
# else:
#     ALLOW_ORIGIN = 'http://122.51.50.135'
#     MYSQL_PWD = os.environ.get("MYSQL_PWD")
ALLOW_ORIGIN = 'http://localhost:8080'
MYSQL_PWD = os.environ.get("MYSQL_PWD")

# from pymemcache.client.base import Client
from flask import Flask, request, make_response, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_cors import CORS
# from flask_httpauth import HTTPTokenAuth

from config import EXPRESS_PRICE_HEADER, UPLOAD_FOLDER, EXPIRE_TIME


# auth = HTTPTokenAuth(scheme='JWT')
# mc_client = Client(('localhost', 11211))
app = Flask(__name__)
# origin不能写为127.0.0.1
# CORS(app, supports_credentials=True, allow_headers='token', expose_headers='token', origins='*')
# CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = secrets.token_hex(16)
serializer = Serializer(app.config['SECRET_KEY'], EXPIRE_TIME)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://express_user:{MYSQL_PWD}@localhost:3306/express?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:Changeme_123@localhost:3306/express?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

@app.before_request
def before_request():
    path = str(request.path)
    print(path)
    if path in ['/login', '/register', '/is-user-exists']:
        return
    # if request.path == '/login' or request.path == '/register':
    #     return
    # https://segmentfault.com/q/1010000012364132
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With, token'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        resp.headers['Access-Control-Allow-Origin'] = ALLOW_ORIGIN
        # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        # resp.headers['Content-Type'] = 'text/plain'
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return resp
    token = request.headers.get('token')
    try:
        # serializer = Serializer(app.config['SECRET_KEY'], EXPIRE_TIME)
        data = serializer.loads(token.encode('utf-8'))
    except:
        abort(401)

@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = ALLOW_ORIGIN
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With, token'
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    resp.headers['Access-Control-Expose-Headers'] = 'token'
    resp.headers['Connection'] = 'keep-alive'
    return resp

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    discount = db.Column(db.Float, default=1.00)

    @staticmethod
    def init_roles():
        if Role.query.all():
            return
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
        role = Role.query.filter_by(name=name).first()
        if not role:
            db.session.add(Role(name=name, discount=discount))
        else:
            role.discount = discount
        db.session.commit()

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # 注册成为黄金会员
    role = db.Column(db.String(64), default='Gold')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        # serializer = Serializer(app.config['SECRET_KEY'], EXPIRE_TIME)
        token = serializer.dumps({'id': self.id, 'username': self.username, 'role': self.role}).decode('utf-8')
        # 双份存储 在before_request和after_request中使用
        # mc_client.set(token, self, EXPIRE_TIME)
        # mc_client.set(self.username, token, EXPIRE_TIME)
        return token

    def verify_token(self, token):
        try:
            data = serializer.loads(token.encode('utf-8'))
        except SignatureExpired:
            self.generate_token()
            return True
        except:
            return False
        return data.get('username') == self.username

    # def confirm(self, token):
    #     try:
    #         data = serializer.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     if data.get('username') != self.username:
    #         return False
    #     self.confirmed = True
    #     db.session.add(self)
    #     db.session.commit()
    #     return True

    # @staticmethod
    # def reset_password(token, new_password):
    #     try:
    #         data = serializer.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     user = Customer.query.get(data.get('id'))
    #     if user is None:
    #         return False
    #     user.password = new_password
    #     db.session.add(user)
    #     db.session.commit()
    #     return True

    @staticmethod
    def register(username, password):
        user = Customer.query.filter_by(username=username).first()
        # user = (True, ) or (False, )
        if user:
            return False
        password_hash = generate_password_hash(password)
        db.session.add(Customer(username=username, password_hash=password_hash))
        db.session.commit()
        return True


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
        if session['user'].role != 'Administrator':
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
        data = ExpressPrice.query.filter_by(from_=row['from_'], to_=row['to_'], name=row['name']).first()
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
    # from_ = request.form.get('from_')
    from_ = 'CN'
    to_ = request.form.get('to_').split('|')[0]
    weight = float(request.form.get('weight'))
    data_set = ExpressPrice.query.filter_by(from_=from_, to_=to_).all()
    result = []
    for data in data_set:
        price_formula = data.price_formula.replace('X', str(weight)).replace('（', '(').replace('）', ')').strip()
        total_price = round(eval(price_formula), 2)
        price = round(total_price / weight, 2)
        result.append({
            'name': data.name,
            # 'from_': data.from_,
            'to_': data.to_,
            'weight': weight,
            'price_formula': price_formula,
            'price': price,
            'currency': 'RMB',
            'total_price': total_price,
            'remarks': data.remarks
        })
    return make_response(jsonify({'expressList': result}), 200)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Customer.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        token = user.generate_token()
        return make_response(jsonify({'isAdmin': user.role == 'Administrator'}), 200, {'token': token})
    return make_response('Username or password is incorrect.', 401)

# @login_required
# @app.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#
# @admin_required
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not Customer().register(username=username, password=password):
        return make_response('Username has been used', 400)
    user = Customer.query.filter_by(username=username).first()
    token = user.generate_token()
    return make_response(jsonify({'isAdmin': False}), 200, {'token': token})

@app.route('/is-user-exists', methods=['POST'])
def is_user_exists():
    username = request.form.get('username')
    print(username)
    user = Customer.query.filter_by(username=username).first()
    print(user)
    if user:
        return make_response(jsonify({'isExists': True}))
    return make_response(jsonify({'isExists': False}))

if __name__ == '__main__':
    # db.session.execute(INIT_DB_SQL)
    # db.session.commit()
    db.create_all()
    Role().init_roles()
    app.run('0.0.0.0', debug=True)
