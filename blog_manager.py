import json
import os
from datetime import datetime
from pathlib import Path
import uuid

class BlogManager:
    def __init__(self, data_file="data/blog_posts.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists and is properly formatted"""
        if not self.data_file.exists():
            self._save_posts([])
    
    def _load_posts(self):
        """Load posts from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_posts(self, posts):
        """Save posts to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error saving posts: {str(e)}")
    
    def create_post(self, title, content, author="Anonymous"):
        """Create a new blog post"""
        posts = self._load_posts()
        
        new_post = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "author": author,
            "created_at": datetime.now().isoformat(),
            "updated_at": None,
            "likes": 0
        }
        
        posts.append(new_post)
        self._save_posts(posts)
        return new_post["id"]
    
    def get_all_posts(self):
        """Get all posts sorted by creation date (newest first)"""
        posts = self._load_posts()
        return sorted(posts, key=lambda x: x['created_at'], reverse=True)
    
    def get_post(self, post_id):
        """Get a specific post by ID"""
        posts = self._load_posts()
        for post in posts:
            if post["id"] == post_id:
                return post
        return None
    
    def update_post(self, post_id, title, content, author):
        """Update an existing post"""
        posts = self._load_posts()
        
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                posts[i].update({
                    "title": title,
                    "content": content,
                    "author": author,
                    "updated_at": datetime.now().isoformat()
                })
                self._save_posts(posts)
                return True
        
        raise Exception("Post not found")
    
    def delete_post(self, post_id):
        """Delete a post by ID"""
        posts = self._load_posts()
        
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                posts.pop(i)
                self._save_posts(posts)
                return True
        
        raise Exception("Post not found")
    
    def get_posts_by_author(self, author):
        """Get all posts by a specific author"""
        posts = self._load_posts()
        return [post for post in posts if post["author"].lower() == author.lower()]
    
    def get_post_count(self):
        """Get total number of posts"""
        return len(self._load_posts())
    
    def like_post(self, post_id):
        """Add a like to a post"""
        posts = self._load_posts()
        
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                posts[i]["likes"] = posts[i].get("likes", 0) + 1
                self._save_posts(posts)
                return posts[i]["likes"]
        
        raise Exception("Post not found")
    
    def unlike_post(self, post_id):
        """Remove a like from a post"""
        posts = self._load_posts()
        
        for i, post in enumerate(posts):
            if post["id"] == post_id:
                current_likes = posts[i].get("likes", 0)
                posts[i]["likes"] = max(0, current_likes - 1)
                self._save_posts(posts)
                return posts[i]["likes"]
        
        raise Exception("Post not found")
    
    def get_total_likes(self):
        """Get total likes across all posts"""
        posts = self._load_posts()
        return sum(post.get("likes", 0) for post in posts)
