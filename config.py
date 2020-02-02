DB_NAME = 'express'
EXPRESS_PRICE_HEADER = ['from_', 'to_', 'name', 'price_formula', 'remarks']
UPLOAD_FOLDER = 'C:'
EXPIRE_TIME = 60 * 60

INIT_DB_SQL = f"""CREATE DATABASE IF NOT EXISTS {DB_NAME};
USE {DB_NAME};
"""