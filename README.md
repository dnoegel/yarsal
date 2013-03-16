# Python interface to the Shopware API

This tiny, inofficial interface to the Shopware API allows you to access the REST API via Python. 

## How to use
Include the library:

        from Shopware.Client import Client

Get an instance of the client:

        client = Client(
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