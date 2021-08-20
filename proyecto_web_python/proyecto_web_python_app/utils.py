from pymongo import MongoClient

client = MongoClient(
    'mongodb+srv://admin:admin@clustertfm.foevo.mongodb.net/tfm?retryWrites=true&w=majority')
db = client['tfm']

