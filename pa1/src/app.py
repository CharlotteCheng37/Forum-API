import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {"id": 0,"upvotes": 1,
        "title": "My cat is the cutest!",
        "link": "https://i.imgur.com/jseZqNK.jpg",
        "username": "alicia98"},
    1: {"id": 1,
        "upvotes": 3,
        "title": "Cat loaf",
        "link": "https://i.imgur.com/TJ46wX4.jpg",
        "username": "alicia98"}
}

comments = {
    0: [{"id": 0,
        "upvotes": 8,
        "text": "Wow, my first Reddit gold!",
        "username": "alicia98"},
        {"id": 1,
         "upvotes": 3, 
         "text": "Nice post!", 
         "username": "bob123"}],
    1: [{"id": 0, 
         "upvotes": 2, 
         "text": "Great read.", 
         "username": "carol"}]  
}

post_id_counter = 2
comment_id_counter = 1
upvotes = 1

# Hello world
@app.route("/")
def hello_world():
    return "Hello world!"


# Get all posts
@app.route("/api/posts/")
def get_post():
    response = {"posts": list(posts.values())}
    return json.dumps(response), 200


# Create a post
@app.route("/api/posts/", methods=["POST"])
def create_post():
    global post_id_counter # if u wanna change a global variable 

    body = json.loads(request.data)
    title = body["title"]
    link = body["link"]
    username = body["username"]

    if not all([title, link, username]):
        return json.dumps({"error": "Missing title, link, or username"}), 400

    post = {"id": post_id_counter,
            "upvotes": upvotes,
            "title": title,
            "link": link,
            "username": username}

    posts[post_id_counter] = post
    comments[post_id_counter] = []
    post_id_counter += 1

    return json.dumps(post), 201


# Get a specific post
@app.route("/api/posts/<int:post_id>/")
def get_post_by_id(post_id):
    post = posts.get(post_id)

    if post is None:
        return json.dumps({"error": "Post is not found"}), 404

    return json.dumps(post), 200
    

# Delete a specific post
@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post(post_id):
    post = posts.get(post_id, None)

    if post is None:
        return json.dumps({"error": "Post is not found"}), 404

    del posts[post_id]
    del comments[post_id] 
    
    return json.dumps(post), 200


# Get comments for a specific post
@app.route("/api/posts/<int:post_id>/comments/")
def get_comment_by_id(post_id):
    post = posts.get(post_id, None)
    if post is None:
        return json.dumps({"error": "Post is not found"}), 404

    post_comments = comments.get(post_id)
    if post_comments is None:
        return json.dumps({"error": "Comment is not found"}), 404

    return json.dumps({"comments": post_comments}), 200


# Post a comment for a specific post
@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def create_comment(post_id):
    global comment_id_counter

    post = posts.get(post_id, None)
    if post is None:
        return json.dumps({"error": "Post is not found"}), 404
    
    body = json.loads(request.data)
    text = body["text"]
    username = body["username"]

    if not all([text, username]):
        return json.dumps({"error": "Missing title, link, or username"}), 400

    comment = {"id": comment_id_counter,
            "upvotes": upvotes,
            "text": text,
            "username": username}

    comments[post_id].append(comment)
    comment_id_counter += 1

    return json.dumps(comment), 201


# Edit a comment for a specific post
@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    post = posts.get(post_id, None)
    if post is None:
        return json.dumps({"error": "Post is not found"}), 404
    
    post_comments = comments.get(post_id)
    if post_comments is None:
        return json.dumps({"error": "Comment is not found"}), 404
    
    body = json.loads(request.data)
    text = body["text"]
    
    for post_comment in post_comments:
        if post_comment["id"] == comment_id:
            post_comment["text"] = text
            return json.dumps(post_comment), 200
        
    return json.dumps({"error": "Comment is not found"}), 404


# Reset Database
@app.route("/api/reset/", methods=["POST"])
def reset_factory_settings():
    global posts, comments, post_id_counter, comment_id_counter, upvotes

    posts = {
        0: {"id": 0, "upvotes": 1,
            "title": "My cat is the cutest!",
            "link": "https://i.imgur.com/jseZqNK.jpg",
            "username": "alicia98"},
        1: {"id": 1,
            "upvotes": 3,
            "title": "Cat loaf",
            "link": "https://i.imgur.com/TJ46wX4.jpg",
            "username": "alicia98"}
    }

    comments = {
        0: [{"id": 0,
             "upvotes": 8,
             "text": "Wow, my first Reddit gold!",
             "username": "alicia98"},
            {"id": 1,
             "upvotes": 3,
             "text": "Nice post!",
             "username": "bob123"}],
        1: [{"id": 0,
             "upvotes": 2,
             "text": "Great read.",
             "username": "carol"}]
    }

    post_id_counter = 2
    comment_id_counter = 1
    upvotes = 1

    return json.dumps({"message": "System reset."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
