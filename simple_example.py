#!/usr/bin/env python3

## Get the logger
# set it to "logging.DEBUG" if you want to see the request URLs generated
# by the script
import logging
logging.basicConfig(level=logging.INFO)

## Get the actual client
import Shopware.Request
from Shopware.Client import SimpleClient



class Example(object):

    def __init__(self):
        ## Get an instance of the client
        self.client = SimpleClient(
            "http://shopware.dev/api",
            "demo",
            "demo"
        )

    def example1(self):
        """Create an article"""

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

        print("Trying to create a article with the number sw-4711")
        try:
            result = self.client.create("articles", data=article)
            print("Our new article has the id {}".format(result['data']['id']))
        except Shopware.Request.SuccessError as e:
            print("Ups - there was an error: {}".format(e.message))

    def example2(self):
        """Search for an article by name

        It is possible to filter any ressource; this way you can search/limit
        the result set
        """

        ## The params array needs to be formated like this:
        params = {
            'filter[0][property]': 'name',
            'filter[0][value]': 'My first article'
        }

        print("Searching for article by name")
        ## Do the actual request
        result = self.client.read("articles", params=params)
        print("{} result found".format(result['total']))
        return result['data']

    def example3(self, articles):
        """Update an article

        Of course partial updates are possible. Here we add an price to our
        article
        """

        ## Get the last id from the article list
        id = articles[-1]['id']

        ## Prepare an article for price update
        article = {
            'mainDetail': {
                'prices': [
                    {
                    'priceGroup': 'EK',
                    'price': 99
                    }
                ]
            }
        }

        try:
            print("Updating the price for the article with the id {}".format(id))
            result = self.client.update("articles", id=id, data=article)
        except Shopware.Request.SuccessError as e:
            print("Ups - there was an error: {}".format(e.message))

    def example4(self):
        """Find a article by its number"""

        print("Accessing the article created above by its number")
        result = self.client.readByNumber('articles', 'sw-4711')
        print("The article with the number sw-4711 hat the name '{}'".format(result['data']['name']))

    def example5(self):
        """Delete an article"""

        ## The params array needs to be formated like this:
        params = {
            'filter[0][property]': 'mainDetail.number',
            'filter[0][value]': 'sw-4711'
        }

        print("Searching for article by main detail id")
        result = self.client.read("articles", params=params)

        ## Actually there can only be one article with a given article number
        for id in (i['id'] for i in result['data']):
            print("Deleting article with id {}".format(id))
            r = self.client.delete('articles', id)
            print(r)


    def benchmark(self):
        import time

        start = time.time()
        todo = 100000
        counter = 0

        # while time.time() <= start+todo:
        while counter <= todo:
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

            try:
                result = self.client.create("articles", data=article)
                counter+=1
                print("{} articles created in {} seconds".format(counter, time.time()-start))
            except Shopware.Request.SuccessError as e:
                print("Ups - there was an error: {}".format(e.message))
                return

        print("Created {} articles in {} seconds".format(counter, time.time()-start))



if __name__ == '__main__':
    app = Example()

    app.benchmark()

    app.example1()
    print("=" * 30)
    articles = app.example2()
    print("=" * 30)
    app.example3(articles)
    print("=" * 30)
    app.example4()
    print("=" * 30)
    app.example5()


