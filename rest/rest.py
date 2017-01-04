from .objects import PathedObject
import requests
import json

def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))

class RestfulAPI(PathedObject):
    def __init__(self, path, headers = None):
        super(RestfulAPI, self).__init__(path)

        self.last = None

        self.joiner = urljoin
        self.headers = headers if headers else {}

        self.headers["Content-Type"] = "application/json"

    def __inherit__(self, newpath):
        return type(self)(newpath, self.headers)

    def __call__(self, **kwargs):
        if kwargs != {}:
            return self.set(self.path, kwargs)
        ret = requests.get(self.path, headers = self.headers)
        self.last = ret
        return [ret.status_code, ret.json()]

    def set(self, path, value):
        ret = requests.post(path, data = json.dumps(value), headers = self.headers)
        self.last = ret

        try:
            obj = ret.json()
        except ValueError:
            obj = {}

        return [ret.status_code, obj]
