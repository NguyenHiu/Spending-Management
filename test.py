import json

class test:
    def __init__(self):
        self.test1 = 123
        self.test2 = '123'
        self.test3 = 'nonn'

    def json_dump(self):
        return {
            "test1": self.test1,
            "test2": self.test2
        }

    def toJson(self):
        return self.json_dump()
        # return json.dumps(self.json_dump())


class parent:
    def __init__(self):
        self.chain = []

    def add(self):
        t = test()
        self.chain.append(t)
        self.chain.append(t)
        self.chain.append(t)

    def toJson(self):
        str = {
            "chain": []
        }
        for i in self.chain:
            str["chain"].append(i.toJson())

        return json.dumps(str)

    def reverse(self, js):
        js = json.loads(js)
        _chain = js["chain"]
        for i in _chain:
            print(i)

# a = parent()
# a.add()
# b = a.toJson()
# print(b)
# a.reverse(b)


# a = b'0x5test'
# print(a.decode('utf-8'))
# # print(bytes(str(a), 'utf-8'))
