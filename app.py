import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# -------------------
# Initialize app
# -------------------
app = Flask(__name__)

# Use Render's DATABASE_URL if provided, fallback to SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///forum.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------
# Database Models
# -------------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

# -------------------
# Routes
# -------------------

# Home page
@app.route("/")
def home():
    return "<h1>Simple Forum API Running</h1><p>Visit <a href='/forum'>/forum</a> to see posts.</p>"

# Simple HTML form to test post creation
@app.route("/test")
def test_form():
    return """
    <form action="/api/posts" method="post">
        <input name="first_name" placeholder="First Name"><br>
        <input name="family_name" placeholder="Family Name"><br>
        <input name="specialty" placeholder="Specialty"><br>
        <button type="submit">Submit</button>
    </form>
    """

# -------------------
# API Endpoints
# -------------------

# Create a post
@app.route("/api/posts", methods=["POST"])
def create_post():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    first_name = data.get("first_name")
    family_name = data.get("family_name")
    specialty = data.get("specialty")

    if not all([first_name, family_name, specialty]):
        return jsonify({"error": "Missing data"}), 400

    post = Post(first_name=first_name, family_name=family_name, specialty=specialty)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created", "id": post.id}), 201

# Get all posts
@app.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {"id": p.id, "first_name": p.first_name, "family_name": p.family_name, "specialty": p.specialty}
        for p in posts
    ])

# Get single post with comments
@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        "id": post.id,
        "first_name": post.first_name,
        "family_name": post.family_name,
        "specialty": post.specialty,
        "comments": [{"id": c.id, "content": c.content} for c in post.comments]
    })

# Add comment to a post
@app.route("/api/posts/<int:post_id>/comments", methods=["POST"])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    if not data or not data.get("content"):
        return jsonify({"error": "Missing comment content"}), 400

    comment = Comment(content=data["content"], post=post)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message": "Comment added"}), 201

# Delete a single post
@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})

# Delete all posts
@app.route("/api/posts/delete_all", methods=["DELETE"])
def delete_all_posts():
    num_deleted = Post.query.delete()
    db.session.commit()
    return jsonify({"message": f"{num_deleted} posts deleted"})

# Forum page (HTML view)
@app.route("/forum")
def forum_page():
    posts = Post.query.all()
    html = "<h1>My Simple Forum</h1>"
    for post in posts:
        html += f"""
        <div style='border:1px solid black; padding:10px; margin:10px'>
            <p><strong>{post.first_name} {post.family_name}</strong> - {post.specialty}</p>
        </div>
        """
    return html

# -------------------
# Run the app
# -------------------
if __name__ == "__main__":
    # Ensure database tables exist
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
