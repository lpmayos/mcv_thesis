class Sense(object):

    def __init__(self, sense, id, sensembed):
        """
        """
        self.sense = sense
        self.id = id
        self.sensembed = sensembed

    def get_sense(self):
        return self.sense

    def get_id(self):
        return self.id

    def get_sensembed(self):
        return self.sensembed
