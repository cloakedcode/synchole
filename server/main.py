from tornado import web
from tornado import ioloop
import app

application = app.SyncHoleApplication('/Users/alan/Hole')

if __name__ == "__main__":
	application.listen(8888)
	ioloop.IOLoop.instance().start()