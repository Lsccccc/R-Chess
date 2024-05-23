class ConditionObj:
    pass

class ConditionExp(ConditionObj):
    def __init__(self, exp: str):
        self.exp = exp

    def exec(self):
        return eval(self.exp)  # TODO

class ConditionSet(ConditionObj):
    types = {
        "AND": all,
        "OR": any
    }
    
    def __init__(self, type=None, subs=[]):
        self.subs = subs
        self.type = type or self.types['AND']

    @classmethod
    def from_json(cls, j: dict):
        """
        example:
        
        j = {
          t: "AND",
          subs: [
            {
              t: "EXP",
              val: "1+1==2"
            },
            {...}
          ]
        }
        """
        def parse_one(d: dict):
            t = d['t']
            if t == "EXP":
                return d['val']

            t = cls.types[t]
            subs = d['subs']
            subs = [parse_one(s) for s in subs]
            return cls(t, subs)

        return parse_one(j)

    def exec(self):
        return self.type(c.exec() for c in self.subs)

    
