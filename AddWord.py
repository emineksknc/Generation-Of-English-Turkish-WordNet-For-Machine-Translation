from neo4j import GraphDatabase
from py2neo.ogm import GraphObject, Property
from py2neo import Graph, NodeMatcher
import pymongo

def WordNetDictionary(English, Turkish, Label):
    uri = "bolt://localhost:11008"
    db = Graph(uri, auth=("neo4j", "123"))
    result = db.run("MATCH (c) "
                    "WHERE c.Literal = {x} and not c.Turkish = {y} and not c.Label = {z} "
                    "SET c.Turkish = c.Turkish + {y}, c.Label = c.Label + {z} "
                    "RETURN c " , x=English, y=Turkish, z=Label ).evaluate()

    print(result)


location = "mongodb://localhost:27017"
client = pymongo.MongoClient(location)
database = client['English-Turkish']
collection = database['English-Turkish']
collection = collection.find()
for mongoWord in collection:
    WordNetDictionary(mongoWord.get("English").lower(),mongoWord.get("Turkish").replace("I", "ı").replace("İ", "i").lower(),mongoWord.get("Label").lower())

