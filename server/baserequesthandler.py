from tornado import web
from tornado import escape

class BaseRequestHandler(web.RequestHandler):
	def renderJson(self, obj):
		callback = self.get_argument('callback', 'callback')
		
		self.set_header("Content-Type", "text/javascript")
		self.finish(callback+'('+escape.json_encode(obj)+')')
