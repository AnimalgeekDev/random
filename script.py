import random
import time
import schedule
from pymongo import MongoClient

def get_mongo_collection():
    return MongoClient(f"mongodb://{username}:{password}@{server}:9001/?authSource=others").get_database("others").get_collection("my_future")

def initialize_db(collection):
    if collection.count_documents({}) == 0:
        options = ["option 1", "opt la quiero menos", "seguro de esto?"]
        collection.insert_many([{"name": option, "weight": 1, "counter": 0} for option in options])

def get_weighted_option(collection, number):
    options = list(collection.find({}, {"_id": 0, "name": 1, "weight": 1}))
    total_weight = sum(opt["weight"] for opt in options)
    threshold = 0
    for option in options:
        threshold += (option["weight"] / total_weight) * 100
        if number <= threshold:
            return option["name"]
    return options[-1]["name"]

def update_counter(collection, option_name):
    collection.update_one({"name": option_name}, {"$inc": {"counter": 1}})

def process():
    collection = get_mongo_collection()
    initialize_db(collection)
    update_counter(collection, get_weighted_option(collection, random.randint(0, 100)))

def main():
    process()
    schedule.every().hour.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)

username = "external"
password = "password"
server = "animalgeek.xyz"

if __name__ == "__main__":
    main()
