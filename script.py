import random
import time
import schedule
from pymongo import MongoClient

def get_mongo_collection(username, password, server, port):
    print(f"Creating client and connecting to mongodb://{username}:{password}@{server}:{port}/?authSource=others")
    client = MongoClient(f"mongodb://{username}:{password}@{server}:{port}/?authSource=others")
    db = client.get_database("others")
    return db.get_collection("myFuture"), db.get_collection("appsConfig")

def initialize_db(collection):
    print("Initializing DB")
    if collection.count_documents({}) == 0:
        print("Creating default options")
        options = ["Desarrollo de video juegos", "Cyberseguridad", "Inteligencia artificial"]
        collection.insert_many([{"name": option, "counter": 0} for option in options])

def get_random_option(max_range, options):
    print("Determining random option")

    range_size = max_range // len(options)
    random_value = random.randint(0, max_range)
    
    if random_value < range_size:
        return options[0]
    elif random_value < 2 * range_size:
        return options[1]
    else:
        return options[2]

def update_counter(collection, option_name):
    print(f"Updating counter for option: {option_name}")
    collection.update_one({"name": option_name}, {"$inc": {"counter": 1}})

def get_app_config(config_collection):
    print("Fetching app configuration")
    config = config_collection.find_one({"appName": "MyFuture"}, {"_id": 0, "maxRange": 1, "timeTrick": 1, "posibleOptions": 1})
    if config:
        return config["maxRange"], config["timeTrick"], config["posibleOptions"]
    else:
        raise ValueError("Configuration for app 'MyFuture' not found")

def process(collection, max_range, options):
    print("Running process")
    initialize_db(collection)
    option = get_random_option(max_range, options)
    update_counter(collection, option)

def main():
    print("Starting...")
    username = "external"
    password = "password"
    server = "mongodb"
    port = "27017"

    collection, config_collection = get_mongo_collection(username, password, server, port)
    max_range, time_trick, options = get_app_config(config_collection)
    
    def scheduled_task():
        process(collection, max_range, options)
    
    print(f"Scheduling task every {time_trick} minutes")
    schedule.every(time_trick).minutes.do(scheduled_task)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
