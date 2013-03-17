import logging

import threading
from time import sleep


import httplib2
from urllib.parse import urlencode
import simplejson

from Shopware.Tasks import ExitTask

class Error(Exception):
    """Base error class for the API"""

class JsonError(Error):
    """This error is raised, when something went wrong decoding the JSON string"""
    def __init__(self, message, error, response):
        Exception.__init__(self, message)
        self.error = error
        self.response = response

class SuccessError(Error):
    """This error is raised, when the request returns success:false"""
    def __init__(self, message, response):
        self.message = message
        self.response = response

class ConnectionError(Error):
    """This error is raised, when httplib request fails"""
    def __init__(self, message, error):
        Exception.__init__(self, message)
        self.error = error



class Request(object):
    """The Request class handled the REST logic

    Usually there is **no need** to have an instance of this class other than
    Shopware.Client().
    """

    def __init__(self, endpoint, user, key):
        self.endpoint = endpoint.rstrip("/").rstrip("\\")
        self.user = user
        self.key = key

        self.noSuccessErrors = True

    def raiseNoSuccessErrors(self, value):
        """If you do not want the interface to raise errors, when the shopware
        API returns 'success:false', call raiseNoSuccessErrors(False)"""

        self.nonSuccessErrors = value

    def request(self, request, resource, id=None, payload='', params=''):
        """Runs a request on the API.

        :param request: Type of the request. One of:

            * GET
            * PUT
            * POST
            * DELETE

        :param resource: Targeted API resource:

            * articles
            * categories
            * customergroups
            * customers
            * media
            * order
            * propertygroups
            * shops
            * translations
            * variants
            * version

        :param id: Optional: Id of the targeted object
        :param payload: For PUT and POST-Requests: Nested array of data
            you want to set
        :param params: Additional params to set. E.g. 'useNumberById' or
            additional filter params. Will be appended to the url.
        :returns: An array with the decoded response of the API.
        """

        url = self.constructUrl(resource, id, params)
        body = simplejson.dumps(payload)
        headers = {'Content-type': 'application/json'}


        logging.debug("Request on url: {}".format(url))
        logging.debug("Headers: {}".format(headers))

        h = httplib2.Http(".cache")
        h.add_credentials(self.user, self.key)
        try:
            response, content = h.request(
                url,
                request,
                body,
                headers
            )
        except Exception as e:
            raise ConnectionError("An error occured during the request", e)

        status = response['status']


        try:
            result =  simplejson.loads(content.decode("utf-8"))
            if not result['success'] and self.noSuccessErrors:
                raise SuccessError(result['message'], result)
            return result
        except simplejson.decoder.JSONDecodeError as e:
            raise JsonError("Error decoding JSON: {}".format(content), e, content)


    def constructUrl(self, resource, id=None, params={}):
        """Constructs a url from the known endpoint, the given resource and
        the given params

        :param resource: The api resource
        :param params: List of additional HTTP params
        :returns: The desired url as string
        """

        if id:
            idString = "/{}/".format(id)
        else:
            idString = '/'
        return self.endpoint + "/" + resource + idString +"?" + urlencode(params)

class ThreadedRequest(threading.Thread, Request):

    def __init__(self, id, queue, endpoint, user, key):
        threading.Thread.__init__(self)

        Request.__init__(self, endpoint, user, key)


        logging.debug("Init thread: {}".format(id))
        self.id = id
        self.queue = queue


    def run(self):
        while True:


            logging.debug("{}: Me got task".format(self.id))
            task = self.queue.get()
            if isinstance(task, ExitTask):
                logging.debug("Recieved exit task")
                return

            try:
                self.request(
                    request=task.request,
                    resource=task.resource,
                    id=task.id,
                    payload=task.data,
                    params=task.param
                )
            except Exception as e:
                if task.errorCallback:
                    task.errorCallback(e, task)
                else:
                    print(e)

            self.queue.task_done()

            if task.successCallback:
                task.successCallback(task)



        # successCallback=None, errorCallback=
