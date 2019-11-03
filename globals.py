from helpers import db
import config

client = None
db = db.Db(config.host, config.username, config.password, config.database, 1)