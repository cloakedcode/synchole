from tornado import web
from tornado import escape
from tornado import ioloop
import urllib
import glob
import os.path
import datetime

class JsonRequestHandler(web.RequestHandler):
	def _renderJson(self, obj):
			callback = self.get_argument('callback', 'callback')
			
			self.set_header("Content-Type", "text/javascript")
			self.finish(callback+'('+escape.json_encode(obj)+')')

class FileHandler(JsonRequestHandler):
	def get(self, dir = ''):
		dir = urllib.unquote(dir)
		path = os.path.abspath(os.path.join(self.application.directory, dir))

		if not path.startswith(self.application.directory) or not os.path.isfile(path):
			raise web.HTTPError(404)

		info = os.stat(path)
		self.set_header("Content-Type", "application/unknown")
		self.set_header("Last-Modified", datetime.datetime.utcfromtimestamp(info.st_mtime))
		object_file = open(path, "r")
		try:
			self._renderJson({'contents': object_file.read()})
		finally:
			object_file.close()

		"""else:
			if not os.path.isdir(path):
				raise web.HTTPError(404)

			files = os.listdir(self.application.directory)
	
			for f in files:
				f = f[len(self.application.directory):]
			self._renderJson({'contents': files})
			"""

	def post(self, path = ''):
		self.put(path)
	
	def put(self, path = ''):
		if not self.request.files:
			raise web.HTTPError(405)

		path = urllib.unquote(path)
		dir = os.path.abspath(os.path.join(self.application.directory, path))

		if not dir.startswith(self.application.directory) or not os.path.isdir(dir):
			raise web.HTTPError(404)
		
		#return self.write(self.request.files)
		for files in self.request.files:
			for f in self.request.files[files]:
				file = os.path.join(dir, f['filename'])

				if os.path.isdir(file):
					raise web.HTTPError(403)

				directory = os.path.dirname(file)
				if not os.path.exists(directory):
					os.makedirs(directory)

				object_file = open(file, "w")
				object_file.write(f['body'])
				object_file.close()

		self.finish()

class SyncHoleApplication(web.Application):
	def __init__(self, root_directory):
		web.Application.__init__(self, [
				#(r"/", RootHandler),
				(r"/files", FileHandler),
				(r"/files/(.*)", FileHandler),
			])

		self.directory = os.path.abspath(root_directory)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

application = SyncHoleApplication('/Users/alan/Hole')

if __name__ == "__main__":
	application.listen(8888)
	ioloop.IOLoop.instance().start()