

class Content:

	class ContentReader:
		def size(self):

	class ContenProvider:
		def reader_at(context, desc):

	class Ingestor:
		def writer(context, opts):

	class ContentInfo:
		content_digest = None
		content_size = None
		content_expected = None
		content_started_at = None
		content_labels = None

	class Status:
		content_ref = None
		content_offset = None
		content_total = None
		content_expected = None
		content_started_at = None
		content_updated_at = None

	class ContentManager:
		def info(self, digest):

		def update(self, info, fieldpaths):

		def walk(self, walk_fn, filters):

		def delete(self, digest):

	class IngestManager:
		def status(self, ref)

		def list_statuses(self, filters)

		def abort(self, ref)

	class ContentWriter:

		def digest(self)

		def commit(self, size, expected, opts)

		def status(self, status, error)

		def truncate(self, size)



	class ContentWriterOpts:
		content_ref = None
		content_desc = None



class Reader:
	reader_digest = None
	reader_size = None
	reader_client = None
	ref = None

	def read_at(self, pos, offset):

	def size(self):
		return self.reader_size

	def close(self):

class Writer:
	writer_client = None
	writer_offset = None
	writer_digest = None
	ref = None

	def send(self, req):

	def status(self):

	def digest(self):

	def write(self, data):

	def commit(self, size, expected, opts):

	def truncate(self, size):

	def close(self):

class ContentStore:
	content_manager = None
	content_provider = None
	ingest_manager = None
	ingester = None

	def __init__(self, client):

	def info(self, digest):

	def walk(self, fn, filters):

	def delete(self, digest):

	def reader_at(self, desc):

	def status(self, ref):

	def update(self, info, fieldpaths):

	def list_statuses(self, filters):

	def writer(self, opts):

	def abort(self, ref):

	def negotiate(self, ref, size, expected):


def info_to_gRPC(info):

def info_from_gRPC(info):

