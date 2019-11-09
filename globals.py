from helpers import db
import config
import redis
client = None
db = db.Db(config.host, config.username, config.password, config.database, 1)
redis = redis.Redis() # configure it yourself