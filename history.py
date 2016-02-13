from collections import defaultdict

class History:
    def __init__(self):
        self.reset()
    def reset(self):
        self.history = defaultdict(list)
    def record(self,actor,action):
        self.history[actor].append(action)
    def getRecords(self,actor=None,action=None):
        if actor:
            if action:
                return [x for x in self.history[actor] if x == action]
            return self.history[actor]
        biglist = []
        for a in self.history:
            biglist += self.history[a]
        if action:
            return [x for x in biglist if x == action]
        return biglist


history = History()
