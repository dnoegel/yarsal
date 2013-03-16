import logging

import httplib2
from urllib.parse import urlencode
import simplejson

class Error(Exception):
    """Base error class for the API"""

class JsonError(Error):
    """This error is raised, when something went wrong decoding the JSON string"""
    pass

class SuccessError(Error):
    """This error is raised, when the request returns success:false"""
    def __init__(self, message, response):
        self.message = message
        self.response = response



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

    def request(self, type, ressource, id=None, payload='', params=''):

        url = self.constructUrl(ressource, id, params)
        body = simplejson.dumps(payload)
        headers = {'Content-type': 'application/json'}


        logging.debug("Request on url: {}".format(url))
        logging.debug("Headers: {}".format(headers))

        h = httplib2.Http(".cache")
        h.add_credentials(self.user, self.key)
        response, content = h.request(
            url,
            type,
            body,
            headers
        )

        status = response['status']


        try:
            result =  simplejson.loads(content.decode("utf-8"))
            if not result['success'] and self.noSuccessErrors:
                raise SuccessError(result['message'], result)
            return result
        except simplejson.decoder.JSONDecodeError as e:
            raise JsonError("Error decoding JSON", e)


    def constructUrl(self, ressource, id=None, params={}):
        """Constructs a url from the known endpoint, the given ressource and
        the given params

        :param ressource: The api ressource
        :param params: List of additional HTTP params
        :returns: The desired url as string
        """

        if id:
            idString = "/{}/".format(id)
        else:
            idString = '/'
        return self.endpoint + "/" + ressource + idString +"?" + urlencode(params)
