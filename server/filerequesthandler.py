from tornado import web
from tornado import escape
import urllib
import os, os.path
import datetime
import baserequesthandler as base

class FileRequestHandler(base.BaseRequestHandler):
	def get(self, file):
		file = urllib.unquote(file)
		path = os.path.abspath(os.path.join(self.application.directory, file))

		if not path.startswith(self.application.directory) or not os.path.isfile(path):
			raise web.HTTPError(404)

		info = os.stat(path)
		self.set_header("Content-Type", "application/unknown")
		self.set_header("Last-Modified", datetime.datetime.utcfromtimestamp(info.st_mtime))
		object_file = open(path, "r")
		try:
			self.finish(object_file.read())
		finally:
			object_file.close()

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
