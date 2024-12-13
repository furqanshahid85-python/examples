import os
import time
import random

import faker
import pymongo


DB_NAME = os.getenv("MONGODB_DB", "imdb")
DB_COLLECTION = os.getenv("MONGODB_COLLECTION", "movies_collection")
DB_USER = os.getenv("MONGODB_USER", "mongo")
DB_PASSWORD = os.getenv("MONGODB_PASSWORD", "mongo")
DB_HOST = os.getenv("MONGODB_HOST", "localhost")
DB_PORT = os.getenv("MONGODB_PORT", "27017")


fake = faker.Faker()


# Function to generate a new sample record
def generate_record():
    return {
        "poster_link": fake.image_url(width=67, height=98),
        "series_title": fake.catch_phrase(),
        "released_year": fake.year(),
        "certificate": random.choice(["A", "B", "C", "D"]),
        "runtime": f"{random.randint(90, 180)} min",
        "genre": random.choice(["Action", "Adventure", "Horror", "Romance", "Sci-fi"]),
        "imdb_rating": round(random.uniform(1.0, 10.0), 1),
        "overview": fake.text(max_nb_chars=1000),
        "meta_score": random.randint(0, 100),
        "director": fake.name(),
        "star1": fake.name(),
        "star2": fake.name(),
        "star3": fake.name(),
        "star4": fake.name(),
        "no_of_votes": random.randint(0, 10000000),
        "gross": fake.pricetag().strip("$"),
    }


# Function to insert a new record into the database
def insert_record(collection, record):
    result = collection.insert_one(record)
    print(f"Record inserted with id: {result.inserted_id}")


# Function to update a record in the database
def update_record(collection, updated_data):
    # Retrieves a random document ID from the MongoDB collection.
    all_ids = list(collection.find({}, {"_id": 1}))
    random_id = random.choice(all_ids)["_id"]

    # Update a record in the MongoDB collection with a random ID.
    filter_criteria = {"_id": random_id}
    result = collection.update_one(filter_criteria, {"$set": updated_data})
    if result.modified_count > 0:
        print(
            f"Record with ID {random_id} updated: {result.modified_count} document(s) modified."
        )
    else:
        print("No records matched the filter criteria.")


def main():
    mongo_client = pymongo.MongoClient(
        f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
    )
    mongo_db = mongo_client[f"{DB_NAME}"]
    mongo_collection = mongo_db[f"{DB_COLLECTION}"]

    print("Connected to the database!")

    # Main loop to continuously insert, update, or delete records
    try:
        while True:
            action = random.choices(["insert", "update"], weights=[0.7, 0.1], k=1)[0]

            if action == "insert":
                new_record = generate_record()
                insert_record(mongo_collection, new_record)
                print("Inserted new record:", new_record)
            elif action == "update":
                updated_record = {
                    "imdb_rating": round(random.uniform(1.0, 10.0), 1),
                    "no_of_votes": random.randint(0, 10000000),
                }
                update_record(mongo_collection, updated_record)

            time.sleep(10)  # Wait for 1 second before the next operation
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
