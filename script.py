import random
import time
import schedule
from pymongo import MongoClient

def get_mongo_collection():
    print(f"Creating client and get connection mongodb://{username}:{password}@{server}:{port}/?authSource=others")
    client = MongoClient(f"mongodb://{username}:{password}@{server}:{port}/?authSource=others")
    db = client.get_database("others")
    return db.get_collection("my_future"), db.get_collection("appsConfig")

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
        threshold += (option["weight"] / total_weight) * max_range
        if number <= threshold:
            return option["name"]
    return options[-1]["name"]

def update_counter(collection, option_name):
    print(f"Update value")
    collection.update_one({"name": option_name}, {"$inc": {"counter": 1}})

def get_app_config(config_collection):
    print("Fetching app configuration")
    config = config_collection.find_one({"appName": "MyFuture"}, {"_id": 0, "maxRange": 1, "timeTrick": 1})
    if config:
        return config["maxRange"], config["timeTrick"]
    else:
        raise ValueError("Configuration for app 'MyFuture' not found")

def process():
    print(f"Run script")
    collection, config_collection = get_mongo_collection()
    initialize_db(collection)
    update_counter(collection, get_weighted_option(collection, random.randint(0, max_range)))

def main():
    global max_range, time_trick
    _, config_collection = get_mongo_collection()
    max_range, time_trick = get_app_config(config_collection)
    process()
    schedule.every(time_trick).minutes.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)

print(f"Start.....")
username = "external"
password = "password"
server = "mongodb"
port = "27017"

max_range = 10
time_trick = 15

if __name__ == "__main__":
    main()