import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['naveen']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, constant1, constant2, new1, new2):
        Database.DATABASE[collection].update_one({constant1: constant2}, {"$set": {new1: new2}})

    @staticmethod
    def delete(collection, query):
        Database.DATABASE[collection].remove(query)



