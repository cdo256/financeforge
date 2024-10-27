from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "9E:&Kt]c}VbK"
app.config['DATABASE_URL'] = "mongodb+srv://devansh88karia:wrQ02Ifp0FfTLZB7@cluster0.pzrjg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
jwt = JWTManager(app)

client = MongoClient(app.config['DATABASE_URL'])
db = client['financeforge']
users_collection = db['users']
progress_collection = db['progress']
topics_collection = db['topics']
subtopics_collection = db['subtopics']

def make_message(message):
    return jsonify({"message": message})

def doc_to_json(document):
    obj = {}
    for key in document:
        if key == '_id':
            obj['id'] = str(document[key])
        elif key == 'password':
            pass
        else:
            obj[key] = document[key]
    return obj

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    if not username:
        return make_message("Parameter 'username' missing"), 400
    if not password:
        return make_message("Parameter 'password' missing"), 400
    if not name:
        return make_message("Parameter 'name' missing"), 400
    
    if users_collection.find_one({"username": username}):
        return make_message("User already exists"), 400

    hashed_password = generate_password_hash(password)
    user_info = {
        "username": username,
        "password": hashed_password,
        "name": name,
        "points": 0,
        "level": 0,
        "progress_percentage": 0
    }
    users_collection.insert_one(user_info)
    user_info = users_collection.find_one({"username": username})
    access_token = create_access_token(identity=username)
    return jsonify(
        access_token=access_token, 
        user_info=doc_to_json(user_info)
    ), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username:
        return make_message("Parameter 'username' missing"), 400
    if not password:
        return make_message("Parameter 'password' missing"), 400
    
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify(
            access_token=access_token,
            user_info=doc_to_json(user)
        ), 200

    return make_message("Invalid credentials"), 401

@app.route('/quiz/<int:topic_id>/<int:subtopic_id>', methods=['POST'])
@jwt_required()
def submit_quiz(topic_id, subtopic_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    user_answers = {int(k): v for k, v in data.get("answers", {}).items()}  # Expecting answers in the format: {"question_id": "selected_option"}

    # Step 1: Calculate score for the quiz
    new_score = calculate_quiz_score(topic_id, subtopic_id, user_answers)

    # Step 2: Update user’s progress with new score if it's higher
    score_updated, message = update_user_progress(current_user, topic_id, subtopic_id, new_score)

    # Step 3: Calculate if topic is complete
    topic_completed, progress_details = calculate_topic_completion(current_user, topic_id)

    # Step 4: Update user level and progress percentage if topic is completed
    if topic_completed:
        update_user_level_and_progress(current_user)
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
    
    quiz_dict = {q["question_id"]: q for q in quiz}

    # Calculate score based on correct answers
    for question_id, user_answer in user_answers.items():
        question = quiz_dict.get(question_id) 
        if question and user_answer == question["correct_option"]:
            score += question["points"]

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
        progress_percentage = ":.2f".format((completed_subtopics / total_subtopics) * 100)
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



@app.route('/questions', methods=['GET'])
@jwt_required()
def get_questions():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"username": current_user})
    print(f'GET QUESTIONS\nusername: {user}')
    with open('questions.txt', 'r') as file:
        data = json.load(file)
    print(len(data))
    return jsonify(data), 201

@app.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"username": current_user})
    
    if user:
        return jsonify({
            "username": current_user,
            "points": user['points'],
            "level": user['level'],
            "progress_percentage": user['progress_percentage']
        }), 200

    return make_message("User not found"), 404

@app.route('/topics', methods=['GET'])
def get_topics():
    topics = topics_collection.find({}, {"_id": 0, "topic_id": 1, "name": 1, "description": 1})
    topics_list = list(topics)
    
    return jsonify(topics_list), 200

@app.route('/topics/<int:topic_id>/subtopics', methods=['GET'])
def get_subtopics(topic_id):
    # Fetch the minimum score for the given topic from the topics collection
    topic = topics_collection.find_one({"topic_id": topic_id})
    if not topic:
        return jsonify({"message": "Topic not found"}), 404
    
    # Fetch all subtopics for the given topic_id
    subtopics = subtopics_collection.find({"topic_id": topic_id})
    subtopics = list(subtopics)
    subtopics_list = []
    quiz_list = []
    for subtopic in subtopics:
        subtopics_list.append({
            "title": subtopic['name'],
            "description": subtopic['content'],
            "id": subtopic['subtopic_id']
        })
        for quiz in subtopic['quiz']:
            quiz_list.append({
                'subtopic_id': subtopic['subtopic_id'],
                'question_id': quiz['question_id'],
                'question_text': quiz['question'],
                'options': quiz['options'],
                'correct_option': quiz['correct_option'],
                'points': quiz['points']
            })
    
    # Add the min_score from the topic to the response
    response = {
        "topic_id": topic_id,
        "min_score": topic["min_score"],
        "subtopics": subtopics_list,
        "questions": quiz_list
    }
    
    return jsonify(response), 200


@app.route('/topics/<int:topic_id>/subtopics/<int:subtopic_id>', methods=['GET'])
def get_subtopic_details(topic_id, subtopic_id):
    # Fetch the specific subtopic by topic_id and subtopic_id
    subtopic = subtopics_collection.find_one(
        {"topic_id": topic_id, "subtopic_id": subtopic_id},
        {"_id": 0, "name": 1, "content": 1, "quiz": 1}
    )
    
    # Check if the subtopic exists
    if not subtopic:
        return jsonify({"message": "Subtopic not found"}), 404
    
    # Format the quiz to include only question_id, question, and options
    formatted_quiz = [
        {
            "question_id": q.get("question_id"),  # Assign a question_id if not already present
            "question": q.get("question"),
            "options": q.get("options")
        }
        for q in subtopic["quiz"]
    ]
    
    # Construct the response
    response = {
        "subtopic_id": subtopic_id,
        "name": subtopic["name"],
        "content": subtopic["content"],
        "quiz": formatted_quiz
    }
    
    return jsonify(response), 200

port = 4000
if os.environ.get('PORT'):
    port = int(os.environ.get('PORT'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)