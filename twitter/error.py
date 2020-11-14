class NoLastPositionData(Exception):
	"""Thrown when no last position data is available for a given query in db.

	Attributes:
		query -- query that has no last position data
		message -- explanation of the error
	"""

	def __init__(self, query, message="No last position data found for this query"):
		self.query = query
		self.message = message
		super().__init__(self.message)

	def __str__(self):
		return f'{self.query} -> {self.message}'

suggestions = {
	"mongo_cannot_connect": "start mongodb"
}
