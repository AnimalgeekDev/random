import random
import time
import schedule
from pymongo import MongoClient

def get_mongo_collection():
    print(f"Creating client and get conection mongodb://{username}:{password}@{server}:9001/?authSource=others")
    return MongoClient(f"mongodb://{username}:{password}@{server}:9001/?authSource=others").get_database("others").get_collection("my_future")

def initialize_db(collection):
    print("Creating DB")
    if collection.count_documents({}) == 0:
        print("Creating default options")
        options = ["Desarrollo de video juegos", "Cyberseguridad", "Inteligencia artificial"]
        collection.insert_many([{"name": option, "weight": 1, "counter": 0} for option in options])

def get_weighted_option(collection, number):
    print("Determinate weight")
    options = list(collection.find({}, {"_id": 0, "name": 1, "weight": 1}))
    total_weight = sum(opt["weight"] for opt in options)
    print(f"Weight {total_weight}")
    threshold = 0
    for option in options:
        threshold += (option["weight"] / total_weight) * 100
        if number <= threshold:
            return option["name"]
    return options[-1]["name"]

def update_counter(collection, option_name):
    print(f"Update value")
    collection.update_one({"name": option_name}, {"$inc": {"counter": 1}})

def process():
    print(f"Run script")
    collection = get_mongo_collection()
    initialize_db(collection)
    update_counter(collection, get_weighted_option(collection, random.randint(0, 100)))

def main():
    process()
    schedule.every().hour.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)

print(f"Start.....")
username = "external"
password = "password"
server = "mongodb"

if __name__ == "__main__":
    main()
