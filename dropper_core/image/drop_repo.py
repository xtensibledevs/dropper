
class DropRepository:
	registery = None
	registery_id = None
	repository_id = None
	org_repo_name = None

	def __init__(self, repo_name):
		if repo_name is None:
			raise Exception('Repository name must be there')
		name_parts = repo_name.split(seperator='/', maxsplit=2)
		self.org_repo_name = repo_name
		if len(name_parts) == 2 && name_parts[0].contains('.') or name_parts[0].contains(':'):
			self.registery_id = name_parts[0]
			self.repository_id = name_parts[1]

		try:
			check_repo(self.repository_id)
		except Exception as ex:
			raise Exception('check_repo error')
		self.registery = registeryapi.Registery(self.registery_id)
		if has_implicit_namespace(self.repository_id, self.registery) and strict==True:
			raise Exception("strict validation required the full repository path(missing 'library')")
		



