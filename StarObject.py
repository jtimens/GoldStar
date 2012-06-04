class starObject:
	issuer = None
	owner = None
	reason = None

	def __init__(self, g, r, rsn):
		self.issuer = g
		self.owner = r
		self.reason = rsn