from datetime import datetime
import re

def format_date(date_string):
    """Format ISO date string to readable format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        return "Unknown date"

def truncate_content(content, max_length=200):
    """Truncate content to specified length with ellipsis"""
    if len(content) <= max_length:
        return content
    
    # Find the last space before max_length to avoid cutting words
    truncated = content[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + "..."

def search_posts(posts, query):
    """Search posts by title, content, or author"""
    if not query:
        return posts
    
    query_lower = query.lower()
    matching_posts = []
    
    for post in posts:
        # Search in title, content, and author
        if (query_lower in post['title'].lower() or 
            query_lower in post['content'].lower() or 
            query_lower in post['author'].lower()):
            matching_posts.append(post)
    
    return matching_posts

def validate_post_data(title, content, author):
    """Validate post data before saving"""
    errors = []
    
    if not title or not title.strip():
        errors.append("Title is required")
    elif len(title.strip()) > 200:
        errors.append("Title must be 200 characters or less")
    
    if not content or not content.strip():
        errors.append("Content is required")
    elif len(content.strip()) > 50000:
        errors.append("Content must be 50,000 characters or less")
    
    if not author or not author.strip():
        errors.append("Author is required")
    elif len(author.strip()) > 100:
        errors.append("Author name must be 100 characters or less")
    
    return errors

def extract_preview_text(content, max_words=50):
    """Extract preview text from content (first N words)"""
    words = content.split()
    if len(words) <= max_words:
        return content
    
    preview_words = words[:max_words]
    return ' '.join(preview_words) + "..."

def count_words(text):
    """Count words in text"""
    return len(text.split())

def count_reading_time(text, words_per_minute=200):
    """Estimate reading time in minutes"""
    word_count = count_words(text)
    reading_time = max(1, round(word_count / words_per_minute))
    return reading_time

def sanitize_filename(filename):
    """Sanitize filename for safe file system usage"""
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    return sanitized or "untitled"
