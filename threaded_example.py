#!/usr/bin/env python3

## Get the logger
import logging
## Set to logging.INFO in order to not have debug output
logging.basicConfig(level=logging.INFO)

import time

## Get the actual client
import Shopware.Request
from Shopware.Client import ThreadedClient



class Example(object):

    def __init__(self):
        self.successCounter = 0
        self.errorCounter = 0


        self.client = ThreadedClient(
            "http://shopware.dev/api",
            "demo",
            "demo",
            numThreads=3
        )

        self.client.setDefaultSuccessCallback(self.successCallback)
        self.client.setDefaultErrorCallback(self.errorCallback)

    def successCallback(self, task):
        self.successCounter += 1
        print("{} articles created in {} seconds, {} errorrs. {} articles/second".format(
            self.successCounter,
            round(time.time()-self.start, 2),
            self.errorCounter,
            round(self.successCounter/(time.time()-self.start), 2)
        ))


    def errorCallback(self, exception, task):
        raise exception
        self.errorCounter += 1

    def benchmark(self):
        import time

        self.start = time.time()

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

            try:
                result = self.client.push(
                    "articles",
                    "POST",
                    data=article
                )

            except Exception as e:
                print("Ups - there was an error: {}".format(e.message))
                self.client.exit()
                return

        print("Put {} tasks to the queue".format(todo))



if __name__ == "__main__":
    app = Example()
    app.benchmark()
