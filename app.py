from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from config import DB_NAME, EXPRESS_PRICE_TABLE, INIT_DB_SQL


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:Changeme_123@localhost:3306'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def init_db():
    db.session.execute(INIT_DB_SQL)
    db.session.execute(f'USE {DB_NAME};')
    db.session.commit()

init_db()

EXPRESS_PRICE_HEADER = ['from_', 'to_', 'express_name', 'price_formula', 'remarks']
def load_excel_rows(file_path):
    import pandas
    data = pandas.read_excel(file_path, names=EXPRESS_PRICE_HEADER)
    for _, row in data.iterrows():
        yield row.values

def _import_express_price(file_path):
    for row in load_excel_rows(file_path):
        sql = f'INSERT INTO {EXPRESS_PRICE_TABLE} SET '
        for key, value in zip(EXPRESS_PRICE_HEADER, row):
            sql += f'{key}="{value}",'
        sql = sql.rstrip(',') + ';'
        db.session.execute(sql)
    db.session.commit()

@app.route('/import-express-price')
def import_express_price():
    _import_express_price('C:\\Users\\Bigshuai-Liu\\Desktop\\py\\logistics-system\\utils\\express_price.xlsx')
    return 'ok'

@app.route('/query')
def query():
    if request.method == 'GET':
        from_ = request.args.get('from_')
        to_ = request.args.get('to_')
        weight = request.args.get('weight')
    else:
        from_ = request.form.get('from_')
        to_ = request.form.get('to_')
        weight = request.form.get('weight')
    keys = ','.join(EXPRESS_PRICE_HEADER).strip(',')
    query_sql = f'select {keys} from {EXPRESS_PRICE_TABLE} where from_="{from_}" and to_="{to_}";'
    for item in db.session.execute(query_sql):
        price_formula = item[3].replace('X', str(weight))
        total_price = round(eval(price_formula), 2)
        print(item[:3], weight, price_formula, total_price, item[-1])
    return 'ok'

if __name__ == '__main__':
    app.run()
