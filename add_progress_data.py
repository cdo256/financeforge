from pymongo import MongoClient
import datetime

# Connect to MongoDB
DATABASE_URL = "mongodb+srv://devansh88karia:wrQ02Ifp0FfTLZB7@cluster0.pzrjg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(DATABASE_URL)
db = client['financeforge']
users_collection = db['users']
progress_collection = db['progress']
subtopics_collection = db['subtopics']

# Dummy users with details
dummy_users = [
    {"username": "alice@example.com", "password": "alice123", "name": "Alice Walker"},
    {"username": "bob@example.com", "password": "bob123", "name": "Bob Martin"},
    {"username": "carol@example.com", "password": "carol123", "name": "Carol Smith"},
    {"username": "david@example.com", "password": "david123", "name": "David Johnson"},
    {"username": "eve@example.com", "password": "eve123", "name": "Eve Brown"},
    {"username": "frank@example.com", "password": "frank123", "name": "Frank Reed"},
    {"username": "grace@example.com", "password": "grace123", "name": "Grace Hall"},
    {"username": "henry@example.com", "password": "henry123", "name": "Henry Clark"},
    {"username": "ivan@example.com", "password": "ivan123", "name": "Ivan Davis"},
    {"username": "julia@example.com", "password": "julia123", "name": "Julia Wilson"},
    {"username": "kate@example.com", "password": "kate123", "name": "Kate Miller"},
    {"username": "liam@example.com", "password": "liam123", "name": "Liam Taylor"},
    {"username": "mike@example.com", "password": "mike123", "name": "Mike Anderson"},
    {"username": "nina@example.com", "password": "nina123", "name": "Nina Martinez"},
    {"username": "olivia@example.com", "password": "olivia123", "name": "Olivia Thomas"},
    {"username": "peter@example.com", "password": "peter123", "name": "Peter Harris"},
    {"username": "quinn@example.com", "password": "quinn123", "name": "Quinn Walker"},
    {"username": "rachel@example.com", "password": "rachel123", "name": "Rachel Scott"},
    {"username": "sam@example.com", "password": "sam123", "name": "Sam Wilson"},
    {"username": "tina@example.com", "password": "tina123", "name": "Tina Anderson"},
]

users_data = [
    {"username": "alice@example.com", "score": 110, "topic_id": 1, "subtopic_id": 2},
    {"username": "alice@example.com", "score": 115, "topic_id": 1, "subtopic_id": 3},
    {"username": "bob@example.com", "score": 200, "topic_id": 2, "subtopic_id": 1},
    {"username": "bob@example.com", "score": 115, "topic_id": 2, "subtopic_id": 2},
    {"username": "carol@example.com", "score": 129, "topic_id": 3, "subtopic_id": 3},
    {"username": "carol@example.com", "score": 80, "topic_id": 3, "subtopic_id": 4},
    {"username": "david@example.com", "score": 180, "topic_id": 1, "subtopic_id": 1},
    {"username": "david@example.com", "score": 370, "topic_id": 1, "subtopic_id": 4},
    {"username": "eve@example.com", "score": 325, "topic_id": 2, "subtopic_id": 5},
    {"username": "frank@example.com", "score": 130, "topic_id": 3, "subtopic_id": 2},
    {"username": "grace@example.com", "score": 141, "topic_id": 2, "subtopic_id": 6},
    {"username": "henry@example.com", "score": 144, "topic_id": 1, "subtopic_id": 5},
    {"username": "ivan@example.com", "score": 90, "topic_id": 3, "subtopic_id": 3},
    {"username": "julia@example.com", "score": 126, "topic_id": 2, "subtopic_id": 4},
    {"username": "kate@example.com", "score": 113, "topic_id": 2, "subtopic_id": 7},
    {"username": "liam@example.com", "score": 219, "topic_id": 3, "subtopic_id": 6},
    {"username": "mike@example.com", "score": 222, "topic_id": 1, "subtopic_id": 6},
    {"username": "nina@example.com", "score": 145, "topic_id": 1, "subtopic_id": 7},
    {"username": "olivia@example.com", "score": 170, "topic_id": 2, "subtopic_id": 8},
    {"username": "peter@example.com", "score": 20, "topic_id": 3, "subtopic_id": 1},
    {"username": "quinn@example.com", "score": 17, "topic_id": 1, "subtopic_id": 8},
    {"username": "rachel@example.com", "score": 16, "topic_id": 3, "subtopic_id": 5},
    {"username": "sam@example.com", "score": 18, "topic_id": 2, "subtopic_id": 1},
    {"username": "tina@example.com", "score": 12, "topic_id": 2, "subtopic_id": 3},
]


def update_user_score_and_progress(user_data):
    username = user_data["username"]
    score = user_data["score"]
    topic_id = user_data["topic_id"]
    subtopic_id = user_data["subtopic_id"]

    # Update the user's total score
    users_collection.update_one(
        {"username": username},
        {"$inc": {"score": score}},
        upsert=True  # Create the user if they don't exist
    )

    # Add a new entry to the progress collection for the subtopic if it doesn't exist
    existing_progress = progress_collection.find_one({
        "username": username,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id
    })

    if existing_progress:
        # Only update score if the new score is higher than the existing score
        if score > existing_progress["score"]:
            progress_collection.update_one(
                {"username": username, "topic_id": topic_id, "subtopic_id": subtopic_id},
                {"$set": {"score": score, "date": datetime.datetime.now()}}
            )
    else:
        # Insert a new record if no existing progress is found
        progress_collection.insert_one({
            "username": username,
            "topic_id": topic_id,
            "subtopic_id": subtopic_id,
            "score": score,
            "date": datetime.datetime.now()
        })

    # Recalculate and update progress percentage
    update_progress_percentage(username)

def update_progress_percentage(username):
    # Calculate total number of subtopics across all topics
    total_subtopics = subtopics_collection.count_documents({})

    # Calculate the number of subtopics the user has completed
    completed_subtopics = progress_collection.count_documents({
        "username": username,
        "type": "subtopic"
    })

    # Calculate and format progress percentage to two decimal places
    if total_subtopics > 0:
        progress_percentage = float("{:.2f}".format((completed_subtopics / total_subtopics) * 100))
    else:
        progress_percentage = 0.0

    # Update the user's progress percentage in the users collection
    users_collection.update_one(
        {"username": username},
        {"$set": {"progress_percentage": progress_percentage}}
    )

for user in dummy_users:
    users_collection.update_one(
        {"username": user["username"]},
        {"$setOnInsert": user},
        upsert=True
    )

for user_data in users_data:
    update_user_score_and_progress(user_data)

print("User scores and progress updated successfully.")
