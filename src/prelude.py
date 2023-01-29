class Logger:
    def __init__(self):
        self.say = lambda msg: print(msg)
        self.info = lambda msg: None

    def verbose(self):
        self.say = lambda msg: print(msg)
        self.info = lambda msg: print(msg)

    def quiet(self):
        self.say = lambda msg: None
        self.info = lambda msg: None

    def moderate(self):
        self.say = lambda msg: print(msg)
        self.info = lambda msg: None

    def say(self, msg):
        self.say(msg)

    def info(self, msg):
        self.info(msg)

logger = Logger()
