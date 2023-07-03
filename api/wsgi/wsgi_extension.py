
class Application(object):
	''' Base WSGI application wrapper. Subclasses need to implement __call__ '''

	@classmethod
	def factory(cls, global_config, **local_config):
		''' Used for paste app factories in paste.deploy config files '''
		return cls(**local_config)

	def __call__(self, environ, start_response):
		''' Subclasses will probably want to implement __call__ like this '''
		raise NotImplementedError("You must implement __call__")

class Middleware(Application):
	''' Base WSGI Middelware '''

	@classmethod
	def factory(cls, global_config, **local_config):
		def _factory(app):
			return cls(app, **local_config)
		return _factory

	def __init__(self, application):
		self.application = application

	def process_request(self, req):
		''' Called on each request '''
		return None

	def process_response(self, response):
		return response

	@webob.dec.wsgify(RequestClass=Request)
	def __call__(self, req):
		response = self.process_request(req)
		if response:
			return response
		response = req.get_response(self.application)
		return self.process_response(response)
