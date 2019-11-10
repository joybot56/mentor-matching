import pymongo


class ManDB:
	"""
	Creating Users
	Updating + Reading Users' Data
	Logging In

	"""
	login_private_key = open("keys/login-db.txt", "r").read().strip()

	def __init__(self, user="andrew", password=None):
		self.client = pymongo.MongoClient(f"mongodb+srv://{user}:{password or open('keys/loginpass.txt').read()}@cluster0-codlf.mongodb.net/test?retryWrites=true&w=majority")
		self.user = user
		self.loginDB = self.client["users"]
		self.loginCol = self.loginDB["login-info"]
	
	def createUser(self, username, password, firstname, lastname, email="e@mail.addr", bio="", school=None, birthdate=25, hobbies=list(), company=None, ethnicity=None, gender=None, position="Lead Systems Engineer", degree="", city="Princeton", state="NJ", ismentor=False, ismentee=False, mentoravailability=False, menteeavailability=False):
		if self.loginCol.find({"email": email}):
			raise Exception("That email address is already taken")
		userProfile = {
			"username": username,
			"password": password,
			"firstname": firstname,
			"lastname": lastname,
			"email": email,
			"bio": bio,
			"school": school,
			"hobbies": hobbies,
			"company": company,
			"ethnicity": ethnicity,
			"gender": gender,
			"position": position,
			"degree": ";".split(degree),
			"location": {
				"city": city,
				"state": state
			},
			"ismentor": ismentor,
			"ismentee": ismentee,
			"mentoravailability": mentoravailability,
			"menteeavailability": menteeavailability
		}
		self.client.insert_one(userProfile)

	def login(self, email, password):
		get_user = self.loginCol.find({"credentials": {"email": email, "password": password}})
		if get_user:
			return email
		else:
			raise Exception("Invalid logon attempt")

	def accessData(self, email):
		get_user = self.loginCol.find_one({"credentials": {"email": email}})
		if get_user:
			return get_user
		else:
			raise Exception("Who are you, really?")
 
		return get_user