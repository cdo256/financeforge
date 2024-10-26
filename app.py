from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
jwt = JWTManager(app)

client = MongoClient(app.config['DATABASE_URL'])
db = client['financeforge']
users_collection = db['users']
progress_collection = db['progress']
topics_collection = db['topics']
subtopics_collection = db['subtopics']

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "points": 0,
        "current_level": 1
    })

    return jsonify({"message": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/quiz/<int:topic_id>/<int:subtopic_id>', methods=['POST'])
@jwt_required()
def submit_quiz(topic_id, subtopic_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    user_answers = data.get("answers")  # Expecting answers in the format: {"question_id": "selected_option"}

    # Step 1: Calculate score for the quiz
    new_score = calculate_quiz_score(topic_id, subtopic_id, user_answers)

    # Step 2: Update user’s progress with new score if it's higher
    score_updated, message = update_user_progress(current_user, topic_id, subtopic_id, new_score)

    # Step 3: Calculate if topic is complete
    topic_completed, progress_details = calculate_topic_completion(current_user, topic_id)

    # Step 4: Update user level and progress percentage if topic is completed
    if topic_completed:
        update_user_level_and_progress(current_user, topic_id)
        return jsonify({
            "message": f"{message} Topic completed!",
            "new_score": new_score,
            "topic_completed": True,
            **progress_details
        }), 200
    else:
        return jsonify({
            "message": message,
            "new_score": new_score,
            "topic_completed": False,
            **progress_details
        }), 200


# Helper Function 1: Calculate Quiz Score
def calculate_quiz_score(topic_id, subtopic_id, user_answers):
    subtopic = subtopics_collection.find_one({"topic_id": topic_id, "subtopic_id": subtopic_id})
    quiz = subtopic["quiz"]
    score = 0

    # Calculate score based on correct answers
    for question in quiz:
        question_id = question["question"]
        correct_option = question["correct_option"]
        points = question["points"]
        if user_answers.get(question_id) == correct_option:
            score += points
    return score


# Helper Function 2: Update User Progress if New Score is Higher
def update_user_progress(username, topic_id, subtopic_id, new_score):
    existing_progress = progress_collection.find_one({
        "username": username,
        "topic_id": topic_id,
        "subtopic_id": subtopic_id
    })

    # Check if new score is higher and update if necessary
    if existing_progress:
        if new_score > existing_progress['score']:
            points_to_add = new_score - existing_progress['score']
            users_collection.update_one(
                {"username": username},
                {"$inc": {"score": points_to_add}}
            )
            progress_collection.update_one(
                {"username": username, "topic_id": topic_id, "subtopic_id": subtopic_id},
                {"$set": {"score": new_score, "date": datetime.datetime.now()}}
            )
            return True, "Score updated to new maximum!"
        else:
            return False, "Score not updated as it's not higher than the previous attempt."
    else:
        # First time submission
        users_collection.update_one(
            {"username": username},
            {"$inc": {"score": new_score}}
        )
        progress_collection.insert_one({
            "username": username,
            "topic_id": topic_id,
            "subtopic_id": subtopic_id,
            "score": new_score,
            "date": datetime.datetime.now()
        })
        return True, "Quiz submitted successfully"


# Helper Function 3: Calculate Topic Completion Status
def calculate_topic_completion(username, topic_id):
    # Retrieve all subtopic scores for the given topic
    user_subtopics = list(progress_collection.find({
        "username": username,
        "topic_id": topic_id
    }))
    
    # Calculate completed subtopics and total score for this topic
    completed_subtopics = len(user_subtopics)
    topic_score = sum(sub["score"] for sub in user_subtopics)

    # Get the total number of subtopics for this topic
    total_subtopics = subtopics_collection.count_documents({"topic_id": topic_id})

    # Retrieve topic details to check minimum score for completion
    topic = topics_collection.find_one({"topic_id": topic_id})
    min_score = topic["min_score"]

    # Step 1: Check if all subtopics are completed
    if completed_subtopics == total_subtopics:
        # Step 2: Check if the score meets the minimum score requirement
        if topic_score >= min_score:
            topic_completed = True
            completion_message = "Topic completed!"
        else:
            topic_completed = False
            completion_message = f"Need {min_score - topic_score} more points to complete the topic."
    else:
        # If not all subtopics are completed, the topic can't be marked as complete
        topic_completed = False
        completion_message = f""

    # Construct progress details
    progress_details = {
        "progress": f"{completed_subtopics}/{total_subtopics} subtopics completed",
        "current_topic_score": topic_score,
        "min_score_for_completion": min_score,
        "completion_message": completion_message
    }

    return topic_completed, progress_details


# Helper Function 4: Update User Level and Progress Percentage
def update_user_level_and_progress(username):
    # Calculate the total number of subtopics across all topics
    total_subtopics = subtopics_collection.count_documents({})
    
    # Calculate the number of completed subtopics for the user
    completed_subtopics = progress_collection.count_documents({"username": username})

    # Calculate the user's progress percentage
    if total_subtopics > 0:
        progress_percentage = (completed_subtopics / total_subtopics) * 100
    else:
        progress_percentage = 0

    # Update user's progress percentage in the users collection
    users_collection.update_one(
        {"username": username},
        {"$set": {"progress_percentage": progress_percentage}}
    )

    # Determine user level based on the number of completed topics
    completed_topics = len(set(progress["topic_id"] for progress in progress_collection.find({"username": username})))
    users_collection.update_one(
        {"username": username},
        {"$set": {"level": completed_topics}}
    )


@app.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"username": current_user})
    
    if user:
        return jsonify({
            "username": current_user,
            "points": user['points'],
            "current_level": user['current_level']
        }), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)