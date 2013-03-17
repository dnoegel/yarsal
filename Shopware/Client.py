import logging
import queue

from Shopware.Request import Request, ThreadedRequest
from Shopware.Tasks import APITask, ExitTask



class SimpleClient(Request):
    """Interface to a shopware shop's API

    :param endpoint: Endpoint of your shopware API,
        e.g. http://www.myshop/api
    :param user: Your backend user name
    :param key: Your API key, configured for each backend user
    """

    def __init__(self, *args, **kwargs):
        Request.__init__(self, *args, **kwargs)

    def create(self, resource, data, params={}):
        """Create a resource

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param data: The data array for your resource
        :param params: Additional params to append to the request *URL*
        """

        return self.request('post', resource, None, data, params)

    def read(self, resource, id=None, params={}):
        """Read a resource

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id: Optional: If set, only the specified object will be feteched
        :param params:
            Additional params to append to the request *URL*
        """

        return self.request('get', resource, id, params=params)

    def update(self, resource, id, data, params={}):
        """Update a given resource

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id: Id of an object to update
        :param params:
            Additional params to append to the request *URL*
        :param data: Nested array of data you want to set.
        """

        return self.request('put', resource, id, data, params=params)

    def delete(self, resource, id, params={}):
        """Delete an object

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id: Id of an object to delete
        :param params: Additional params to append to the request *URL*
        """

        return self.request('delete', resource, id, params=params)

    def updateByNumber(self, resource, id, data, params = {}):
        """Convenience method to update a given resource by its number.

        Same as calling update(resource, id, data, params={'useNumberAsId'=True})

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id:  Id of an object to update
        :param data: Nested array of data you want to set.
        :param params: Additional params to append to the request *URL*
        """

        params['useNumberAsId'] = True
        return  self.update(resource, id, data, params=params)

    def deleteByNumber(self, resource, id, params = {}):
        """Convenience method to delete a given resource by its number

        Same as calling delete(resource, id, params={'useNumberAsId'=True})

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id: Id of an object to delete
        :param params: Additional params to append to the request *URL*
        """

        params['useNumberAsId'] = True
        return self.delete(resource, id, params=params)

    def readByNumber(self, resource, id, params = {}):
        """Convenience method to read a given resource by its number

        Same as calling read(resource, id, params={'useNumberAsId'=True})

        :param resource: Any existing API resource. Default Shopware resource are:

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

            As the shopware API can be extended by plugins, any of those
            resource might work as well
        :param id: Id of an object to read
        :param params: Additional params to append to the request *URL*
        """


        params['useNumberAsId'] = True
        return self.read(resource, id, params=params)

class ThreadedClient(object):
    """The threaded client allows you to query the API asynchronous

    **General**

    You can add requests with the **push** method. The ThreadedClient will
    create a Task from your Request, add it to a queue and let *numThreads*
    request-threads handle this queue.

    In order to be notified when a given request was handled, you can register
    callback functions: You can register callbacks for any successfull request
    and callbacks for any request which was not successfull.

    **Performance impacts**

    As the Shopware API currently needs a single request for any operation,
    having multiple threads might help you, to compensate the latency which
    originates from this whole waiting-for-answer thing.

    This, however, also will raise the load of your servers, so you should
    keep an eye on thise while increasing the number of threads used by this
    script.

    :param endpoint: API endpoint, e.g. http://www.shopware.dev/api
    :param user: API user
    :param key: API user's key
    :param numThreads: Number of threads to spawn

    """

    def __init__(self, endpoint, user, key, numThreads=3):
        self.endpoint = endpoint
        self.user = user
        self.key = key

        self.numThreads = numThreads
        self.queue = queue.Queue()

        self.defaultSuccessCallback = None
        self.defaultErrorCallback = None

        self.spawnThreads()

    def spawnThreads(self):
        """Internal helper function to spawn the configured number of threads"""

        self.threads = []
        for id in range(self.numThreads):
            thread = ThreadedRequest(
                id,
                self.queue,
                self.endpoint,
                self.user,
                self.key
            )
            thread.start()
            self.threads.append(thread)

    def exit(self):
        """Clear the queue and put exit tasks into it"""

        ## Empty the queue
        try:
            while self.queue.get(block=False):
                pass
        except queue.Empty:
            pass

        ## Push ExitTasks
        for i in range(self.numThreads):
            self.queue.put(ExitTask())



    def setDefaultSuccessCallback(self, callback):
        """Set the default callback for successfull taks.

        Will be added to any request if no other successCallback is defined
        """

        self.defaultSuccessCallback = callback

    def setDefaultErrorCallback(self, callback):
        """Set the default callback for tasks with errors.

        Will be added to any requerst unless another errorCallback is defined
        """

        self.defaultErrorCallback = callback

    def push(self, resource, action='GET', id=None, data=None, params={},
        successCallback=None, errorCallback=None):
        """Push a task to the queue

        Adds a new taks to the queue which is processed by the threaded request
        objects.

        :param resource: API resource to query, e.g. 'articles'
        :param action: which action do you want to trigger?

            * GET
            * POST
            * PUT
            * DELETE

        :param id: Id of the object to read/delete/update
        :param data: Data you want to send
        :param params: Additional params to add to the url
        :param successCallback: Function to be called if the request was process
        successfully
        :param errorCallback: Function to be called if an error occurred
        """

        ## Get default success/error callbacks if non was passed here
        if not successCallback:
            successCallback = self.defaultSuccessCallback
        if not errorCallback:
            errorCallback = self.defaultErrorCallback

        ## Create a task object
        t = APITask(resource, action, id, data, params,
            successCallback=successCallback, errorCallback=errorCallback
        )

        ## Push the task to queue
        self.queue.put(t)


