class Token(object):

    def __init__(self, token, id, senses_list=[]):
        """
        """
        self.token = token
        self.id = id
        self.senses = senses_list

    def get_token(self):
        return self.token

    def get_id(self):
        return self.id

    def get_senses(self):
        return self.senses

    def addSense(self, sense):
        self.senses.append(sense)
