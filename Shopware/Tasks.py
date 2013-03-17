class BaseTask(object):
    pass

class APITask(BaseTask):

    def __init__(self, resource, request="GET", id=None, data=None, param={},
    successCallback=None, errorCallback=None):

        self.resource = resource
        self.request = request
        self.id = id
        self.data = data
        self.param = param

        self.successCallback = successCallback
        self.errorCallback = errorCallback


    def nase():
        print("nase")


class ExitTask(BaseTask): pass
