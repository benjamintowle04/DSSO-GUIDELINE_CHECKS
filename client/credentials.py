class Credentials:
    def __init__(self, code, user, password):
        self.code = code
        self.user = user
        self.password = password

def load_creds():
	creds = Credentials("isu", "program", "123456789")
	return creds