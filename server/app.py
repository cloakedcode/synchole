from tornado import web
import filerequesthandler as file
import os, os.path

class SyncHoleApplication(web.Application):
	def __init__(self, root_directory):
		web.Application.__init__(self, [
				#(r"/", RootHandler),
				(r"/files", file.FileRequestHandler),
				(r"/files/(.*)", file.FileRequestHandler),
			])

		self.directory = os.path.abspath(root_directory)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)
