import logging

from Shopware.Request import Request


class Client(Request):
    """Interface to a shopware shop's API

    :param endpoint: Endpoint of your shopware API,
        e.g. http://www.myshop/api
    :param user: Your backend user name
    :param key: Your API key, configured for each backend user
    """

    def __init__(self, *args):
        Request.__init__(self, *args)

    def create(self, ressource, data, params={}):
        """Create a ressource

        :param ressource: Any existing API ressource.
            Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param data:
            The data array for your ressource
        :param params:
            Additional params to append to the request *URL*
        """

        return self.request('post', ressource, None, data, params)

    def read(self, ressource, id=None, params={}):
        """Read a ressource

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id: Optional: If set, only the specified object will be feteched
        :param params:
            Additional params to append to the request *URL*
        """

        return self.request('get', ressource, id, params=params)

    def update(self, ressource, id, data, params={}):
        """Update a given ressource

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id: Id of an object to update
        :param params:
            Additional params to append to the request *URL*
        """

        return self.request('put', ressource, id, data, params=params)

    def delete(self, ressource, id, params={}):
        """Delete an object

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id: Id of an object to delete
        :param params:
            Additional params to append to the request *URL*
        """

        return self.request('delete', ressource, id, params=params)

    def updateByNumber(self, ressource, id, data):
        """Convenience method to update a given ressource by its number.

        Same as calling update(ressource, id, data, params={'useNumberAsId'=True})

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id:  Id of an object to update

        """

        params['useNumberAsId'] = True
        return  self.update(ressource, id, data, params=params)

    def deleteByNumber(self, ressource, id, ):
        """Convenience method to delete a given ressource by its number

        Same as calling delete(ressource, id, params={'useNumberAsId'=True})

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id: Id of an object to delete
        """

        params['useNumberAsId'] = True
        return self.delete(ressource, id, params=params)

    def readByNumber(self, ressource, id, params = {}):
        """Convenience method to read a given ressource by its number

        Same as calling read(ressource, id, params={'useNumberAsId'=True})

        :param ressource:
            Any existing API ressource. Default Shopware ressource are:
                * articles
                * customers
                * categories
                * media
                * variants
                * orders
            As the shopware API can be extended by plugins, any of those
            ressource might work as well
        :param id: Id of an object to read
        """


        params['useNumberAsId'] = True
        return self.read(ressource, id, params=params)
