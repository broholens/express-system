"""
TODO:
1. 数据库密码从env中获取
"""
import os

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from flask_cors import CORS

from config import EXPRESS_PRICE_TABLE, EXPRESS_PRICE_HEADER, UPLOAD_FOLDER, INIT_DB_SQL


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Changeme_123@localhost:3306'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
db.session.execute(INIT_DB_SQL)
db.session.commit()

class ExpressPrice(db.Model):
    __tablename__ = EXPRESS_PRICE_TABLE
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_ = db.Column(db.String(16), nullable=False, index=True)
    to_ = db.Column(db.String(16), nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True)
    price_formula = db.Column(db.String(40), default='X')
    remarks = db.Column(db.Text)

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
            ExpressPrice.name == row['name'],
            ExpressPrice.price_formula == row['price_formula'],
            ExpressPrice.remarks == row['remarks']
        ).first()
        if not data:
            db.session.add(ExpressPrice(**row))
    db.session.commit()

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


if __name__ == '__main__':
    db.create_all()
    app.run()
