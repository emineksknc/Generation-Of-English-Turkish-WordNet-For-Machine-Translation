from neo4j import GraphDatabase
from py2neo.ogm import GraphObject, Property
from py2neo import Graph, NodeMatcher
import pymongo

def WordNetDictionary(English, Turkish, Label):
    uri = "bolt://localhost:11008"
    db = Graph(uri, auth=("neo4j", "123"))
    result = db.run("MATCH (c) "
                    "WHERE c.Literal = {x} "
                    "SET c.Turkish = {y}, c.Label = {z}"
                    "RETURN c", x=English, y=Turkish, z=Label ).evaluate()

    print(result)



def MongoDbDictionary(dictionaryWord):
    location = "mongodb://localhost:27017"
    client = pymongo.MongoClient(location)
    database = client['English-Turkish']
    collection = database['English-Turkish']
    collection = collection.find()
    for mongoWord in collection:
        if mongoWord.get("English") == dictionaryWord:
            WordNetDictionary(mongoWord.get("English").lower(),mongoWord.get("Turkish").replace("I", "ı").replace("İ", "i").lower(),mongoWord.get("Label").lower())



file = open("dictionary.txt", "r")  # English-Turkish dictionary
dictionary = file.readlines()
sorting_word = []

for word in dictionary:
    if word.find("\t") != False:
        english_turkish = dict(English=word.split("\t")[0], Turkish=word.split("\t")[1],
                                   Label=word.split("\t")[2].replace("\n", " "))

        sorting_word.append(english_turkish["English"])




for dictionaryWord in sorting_word:
    count = sorting_word.count(dictionaryWord)
    if count == 1:
        MongoDbDictionary(dictionaryWord)




