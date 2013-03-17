# Yet another ridiculously slim API layer 

This is an inofficial, very basic interface to the Shopware REST API. It offers a *SimpleClient* which basically wraps the underlying HTTP requests and a *ThreadedClient* which lets you process your tasks with multiple HTTP requests at the same time.

## How to use
### SimpleClient
The SimpleClient basically offers some convenience functions wrapped around the underlying HTTP library.

Include the library:

        from Shopware.Client import SimpleClient

Get an instance of the client:

        client = SimpleClient(
            "http://shopware.dev/api",
            "demo",
            "demo"
        )

Fire a request:

        article = {
            "name": "My first article",
            "description": "I am so proud of it o_Ô",
            "tax": "19",
            "mainDetail": {
                "number": "sw-4711",
                "active": True,
                "prices": [
                    {
                    "priceGroup": 'EK',
                    "price": 999
                    }
                ]
            }
        }
        result = self.client.create("articles", data=article)

### ThreadedClient
The ThreadedClient creates a queue for your tasks and a given number of worker threads eagerly waiting for the queue to be filled. 

In order to know if a task succeeded (or not), you are able to define callback-functions. If you want to have global callback functions for all your task, make use of the methods **setDefaultSuccessCallback** and **setDefaultErrorCallback** of the ThreadedClient. If you want to have specific callback functions (e.g. a callback function for customers, a callback function for articles...) you can also define callbacks for each request via the **push** method of ThreadedClient.

Please keep in mind, that the callback functions are triggered by the worker thread, that handled the given task. For that reason, you might want to implement additional logic, if your further logic is not thread safe. Queues are a good idea here.

Include the library:

        from Shopware.Client import ThreadedClient

Get an instance of the client:

        client = ThreadedClient(
            "http://shopware.dev/api",
            "demo",
            "demo",
            numThreads=3
        )

Define Callbacks:

        client.setDefaultSuccessCallback(successCallback)
        client.setDefaultErrorCallback(errorCallback)

Implement Callbacks:

    def successCallback(task):
        print(task.data['mainDetail']['number'])

    def errorCallback(exception, task):
        print("There was an error updating: Resource: {}, Request: {}".format(
            task.resource,
            task.request
        ))

Run a lot of requests:

        todo = 100000

        for i in range(todo):
            number = "sw-{}".format(time.time())
            article = {
                "name": "My first article",
                "description": "I am so proud of it o_Ô",
                "tax": "19",
                "mainDetail": {
                    "number": number,
                    "active": True,
                    "prices": [
                        {
                        "priceGroup": 'EK',
                        "price": 999
                        }
                    ]
                }
            }

            result = self.client.push(
                "articles",
                "POST",
                data=article
            )

## Request types
The interface is quite generic, so you can use any resource of the Shopware API. Additional resources, offered by 3rd party plugins, are most probably also supported.

Default resources (SW 4.0.7.) are:

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

## Handling errors
By default, there are four types of errors raised by this interface:

 * **Shopware.Request.Error** Default error type. All other errors inherit from this class.
 * **Shopware.Request.JsonError** Raised when the API returns a string which cannot be parsed as JSON string.
 * **Shopware.Request.SuccessError** Raised when the API returns an array having success=false. You can prevent the Interface from raising this error, by calling raiseNoSuccessErrors(False) on the client.
 * **Shopware.Request.ConnectionError** Raised when the actual Request fails (e.g. socket or httplib errors)

## Examples

Examples can be found in **example.py**. 
