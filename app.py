import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from blog_manager import BlogManager
from utils import format_date, truncate_content, search_posts

# Initialize blog manager
blog_manager = BlogManager()

# Configure page
st.set_page_config(
    page_title="Personal Blog",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dynamic CSS for light/dark mode
def get_theme_css():
    if st.session_state.dark_mode:
        return """
        <style>
            .stApp {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            
            .main-header {
                background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%);
                padding: 2rem 1rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
            }
            
            .post-container {
                background: #2d3748;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 1.5rem;
                border-left: 4px solid #4a5568;
            }
            
            .post-title {
                color: #e2e8f0;
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .post-meta {
                color: #a0aec0;
                font-size: 0.9rem;
                margin-bottom: 1rem;
            }
            
            .post-content {
                color: #cbd5e0;
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            
            .sidebar-header {
                background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                color: white;
                text-align: center;
            }
            
            .stats-container {
                background: #2d3748;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                color: #e2e8f0;
            }
            
            .welcome-banner {
                background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .search-highlight {
                background: #744210;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                border-left: 4px solid #f6e05e;
                margin-bottom: 1rem;
                color: #faf089;
            }
            
            .empty-state {
                text-align: center;
                padding: 3rem;
                color: #a0aec0;
            }
            
            .form-container {
                background: #2d3748;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 2rem;
            }
            
            .manage-post-item {
                background: #2d3748;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.3);
                margin-bottom: 1rem;
                border-left: 3px solid #4a5568;
            }
            
            .reading-time {
                color: #a0aec0;
                font-size: 0.85rem;
                font-style: italic;
            }
            
            .like-button {
                background: none;
                border: none;
                color: #e53e3e;
                cursor: pointer;
                font-size: 1.2rem;
                margin-right: 0.5rem;
            }
            
            .like-button:hover {
                color: #c53030;
            }
            
            .like-count {
                color: #a0aec0;
                font-size: 0.9rem;
            }
        </style>
        """
    else:
        return """
        <style>
            .main-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                padding: 2rem 1rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
            }
            
            .post-container {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 1.5rem;
                border-left: 4px solid #667eea;
            }
            
            .post-title {
                color: #2c3e50;
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .post-meta {
                color: #7f8c8d;
                font-size: 0.9rem;
                margin-bottom: 1rem;
            }
            
            .post-content {
                color: #34495e;
                line-height: 1.6;
                margin-bottom: 1rem;
            }
            
            .sidebar-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                color: white;
                text-align: center;
            }
            
            .stats-container {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            
            .welcome-banner {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .button-container {
                display: flex;
                gap: 10px;
                margin-top: 1rem;
            }
            
            .pagination-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin: 2rem 0;
            }
            
            .search-highlight {
                background: #fff3cd;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
                margin-bottom: 1rem;
            }
            
            .empty-state {
                text-align: center;
                padding: 3rem;
                color: #6c757d;
            }
            
            .form-container {
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
            }
            
            .manage-post-item {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
                border-left: 3px solid #667eea;
            }
            
            .reading-time {
                color: #6c757d;
                font-size: 0.85rem;
                font-style: italic;
            }
            
            .like-button {
                background: none;
                border: none;
                color: #e53e3e;
                cursor: pointer;
                font-size: 1.2rem;
                margin-right: 0.5rem;
            }
            
            .like-button:hover {
                color: #c53030;
            }
            
            .like-count {
                color: #6c757d;
                font-size: 0.9rem;
            }
        </style>
        """

# Initialize session state FIRST
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'current_post_id' not in st.session_state:
    st.session_state.current_post_id = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'posts_per_page' not in st.session_state:
    st.session_state.posts_per_page = 5
if 'current_page_num' not in st.session_state:
    st.session_state.current_page_num = 1
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'liked_posts' not in st.session_state:
    st.session_state.liked_posts = set()

# Apply theme CSS AFTER session state is initialized
st.markdown(get_theme_css(), unsafe_allow_html=True)

def navigate_to(page, post_id=None):
    """Navigate to a specific page"""
    st.session_state.current_page = page
    if post_id:
        st.session_state.current_post_id = post_id
    st.rerun()

def main():
    # Enhanced sidebar navigation with custom styling
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h2>📝 Personal Blog</h2>
        <p>Your digital writing space</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    if st.sidebar.button("🏠 Home", use_container_width=True):
        navigate_to("home")
    
    if st.sidebar.button("✍️ Write New Post", use_container_width=True):
        navigate_to("create")
    
    if st.sidebar.button("📋 Manage Posts", use_container_width=True):
        navigate_to("manage")
    
    
    # Enhanced search functionality
    st.sidebar.markdown("### 🔍 Search")
    search_query = st.sidebar.text_input("Search posts...", value=st.session_state.search_query, placeholder="Enter keywords...")
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.session_state.current_page_num = 1
        st.rerun()
    
    # Blog statistics
    total_posts = blog_manager.get_post_count()
    total_likes = blog_manager.get_total_likes()
    st.sidebar.markdown(f"""
    <div class="stats-container">
        <h4>📊 Blog Stats</h4>
        <p><strong>Total Posts:</strong> {total_posts}</p>
        <p><strong>Total Likes:</strong> ❤️ {total_likes}</p>
        <p><strong>Page:</strong> {st.session_state.current_page_num}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings section
    st.sidebar.markdown("### ⚙️ Settings")
    
    # Dark mode toggle
    if st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark_mode else "☀️ Toggle Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    
    # Posts per page setting
    posts_per_page = st.sidebar.selectbox(
        "Posts per page:",
        [3, 5, 10, 15],
        index=[3, 5, 10, 15].index(st.session_state.posts_per_page)
    )
    if posts_per_page != st.session_state.posts_per_page:
        st.session_state.posts_per_page = posts_per_page
        st.session_state.current_page_num = 1
        st.rerun()
    
    # Main content area
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "create":
        show_create_page()
    elif st.session_state.current_page == "edit":
        show_edit_page()
    elif st.session_state.current_page == "manage":
        show_manage_page()
    elif st.session_state.current_page == "view":
        show_view_page()

def show_home_page():
    """Display the home page with blog posts"""
    # Enhanced welcome header
    st.markdown("""
    <div class="welcome-banner">
        <h1>🌟 Welcome to My Personal Blog</h1>
        <p>Discover thoughts, ideas, and stories from my digital journal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all posts
    all_posts = blog_manager.get_all_posts()
    
    # Apply search filter if query exists
    if st.session_state.search_query:
        all_posts = search_posts(all_posts, st.session_state.search_query)
        if all_posts:
            st.markdown(f"""
            <div class="search-highlight">
                <strong>🔍 Search Results:</strong> Found {len(all_posts)} post(s) matching '{st.session_state.search_query}'
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="empty-state">
                <h3>🔍 No Results Found</h3>
                <p>No posts found matching '{st.session_state.search_query}'</p>
                <p>Try different keywords or browse all posts</p>
            </div>
            """, unsafe_allow_html=True)
            return
    
    if not all_posts:
        st.markdown("""
        <div class="empty-state">
            <h3>📝 No Posts Yet</h3>
            <p>Your blog is waiting for your first story!</p>
            <p>Click 'Write New Post' in the sidebar to get started</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Pagination
    total_posts = len(all_posts)
    total_pages = (total_posts - 1) // st.session_state.posts_per_page + 1
    
    # Enhanced pagination controls
    st.markdown("""
    <div class="pagination-container">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page_num > 1:
            if st.button("← Previous", type="secondary"):
                st.session_state.current_page_num -= 1
                st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align: center; padding: 10px;'><strong>Page {st.session_state.current_page_num} of {total_pages}</strong></div>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_page_num < total_pages:
            if st.button("Next →", type="secondary"):
                st.session_state.current_page_num += 1
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculate start and end indices for current page
    start_idx = (st.session_state.current_page_num - 1) * st.session_state.posts_per_page
    end_idx = start_idx + st.session_state.posts_per_page
    posts_to_show = all_posts[start_idx:end_idx]
    
    # Display posts with enhanced styling
    for post in posts_to_show:
        # Import utils for reading time calculation
        from utils import count_reading_time
        reading_time = count_reading_time(post['content'])
        likes_count = post.get('likes', 0)
        
        st.markdown(f"""
        <div class="post-container">
            <div class="post-title">{post['title']}</div>
            <div class="post-meta">
                📅 {format_date(post['created_at'])} | 
                👤 {post['author']} | 
                <span class="reading-time">⏱️ {reading_time} min read</span> |
                ❤️ {likes_count} likes
            </div>
            <div class="post-content">
                {truncate_content(post['content'], 200)}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button(f"📖 Read More", key=f"read_{post['id']}", type="primary"):
                navigate_to("view", post['id'])
        with col2:
            # Like button
            like_icon = "❤️" if post['id'] in st.session_state.liked_posts else "🤍"
            if st.button(f"{like_icon} Like", key=f"like_{post['id']}", type="secondary"):
                if post['id'] in st.session_state.liked_posts:
                    blog_manager.unlike_post(post['id'])
                    st.session_state.liked_posts.remove(post['id'])
                else:
                    blog_manager.like_post(post['id'])
                    st.session_state.liked_posts.add(post['id'])
                st.rerun()

def show_create_page():
    """Display the create post page"""
    st.markdown("""
    <div class="main-header">
        <h1>✍️ Write New Post</h1>
        <p>Share your thoughts with the world</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("create_post_form"):
        title = st.text_input("📝 Post Title", placeholder="Enter your post title...")
        author = st.text_input("👤 Author", value="Anonymous", placeholder="Your name...")
        content = st.text_area("📄 Content", height=300, placeholder="Write your post content here...")
        
        # Show word count
        if content:
            word_count = len(content.split())
            reading_time = max(1, round(word_count / 200))
            st.markdown(f"<small>📊 Words: {word_count} | ⏱️ Reading time: ~{reading_time} min</small>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📝 Publish Post", type="primary")
        
        if submitted:
            if not title.strip():
                st.error("Please enter a title for your post.")
            elif not content.strip():
                st.error("Please enter content for your post.")
            else:
                try:
                    post_id = blog_manager.create_post(title.strip(), content.strip(), author.strip())
                    st.success(f"🎉 Post '{title}' published successfully!")
                    st.info("Redirecting to home page...")
                    st.balloons()
                    # Add a small delay before redirect
                    import time
                    time.sleep(1)
                    navigate_to("home")
                except Exception as e:
                    st.error(f"❌ Error creating post: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back to home button
    if st.button("← Back to Home", type="secondary"):
        navigate_to("home")

def show_edit_page():
    """Display the edit post page"""
    if not st.session_state.current_post_id:
        st.error("No post selected for editing.")
        if st.button("← Back to Home"):
            navigate_to("home")
        return
    
    post = blog_manager.get_post(st.session_state.current_post_id)
    if not post:
        st.error("Post not found.")
        if st.button("← Back to Home"):
            navigate_to("home")
        return
    
    st.markdown(f"""
    <div class="main-header">
        <h1>✏️ Edit Post</h1>
        <p>Make changes to "{post['title']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("edit_post_form"):
        title = st.text_input("📝 Post Title", value=post['title'])
        author = st.text_input("👤 Author", value=post['author'])
        content = st.text_area("📄 Content", value=post['content'], height=300)
        
        # Show word count
        if content:
            word_count = len(content.split())
            reading_time = max(1, round(word_count / 200))
            st.markdown(f"<small>📊 Words: {word_count} | ⏱️ Reading time: ~{reading_time} min</small>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Update Post", type="primary")
        with col2:
            cancel = st.form_submit_button("❌ Cancel", type="secondary")
        
        if submitted:
            if not title.strip():
                st.error("Please enter a title for your post.")
            elif not content.strip():
                st.error("Please enter content for your post.")
            else:
                try:
                    blog_manager.update_post(st.session_state.current_post_id, title.strip(), content.strip(), author.strip())
                    st.success("🎉 Post updated successfully!")
                    st.info("Redirecting to home page...")
                    import time
                    time.sleep(1)
                    navigate_to("home")
                except Exception as e:
                    st.error(f"❌ Error updating post: {str(e)}")
        
        if cancel:
            navigate_to("home")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_manage_page():
    """Display the manage posts page"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Manage Posts</h1>
        <p>Edit, delete, and organize your content</p>
    </div>
    """, unsafe_allow_html=True)
    
    posts = blog_manager.get_all_posts()
    
    if not posts:
        st.markdown("""
        <div class="empty-state">
            <h3>📝 No Posts to Manage</h3>
            <p>Create your first post to see it here</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back to Home", type="secondary"):
            navigate_to("home")
        return
    
    st.markdown(f"<div class='stats-container'><h4>📊 Total Posts: {len(posts)}</h4></div>", unsafe_allow_html=True)
    
    # Display posts in enhanced format
    for post in posts:
        from utils import count_reading_time
        reading_time = count_reading_time(post['content'])
        likes_count = post.get('likes', 0)
        
        st.markdown(f"""
        <div class="manage-post-item">
            <div class="post-title">{post['title']}</div>
            <div class="post-meta">
                👤 {post['author']} | 📅 {format_date(post['created_at'])} | ⏱️ {reading_time} min read | ❤️ {likes_count} likes
            </div>
            {f'<div class="post-meta">📝 Updated: {format_date(post["updated_at"])}</div>' if post['updated_at'] else ''}
            <div class="post-content">{truncate_content(post['content'], 100)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            if st.button("✏️ Edit", key=f"edit_{post['id']}", type="secondary"):
                navigate_to("edit", post['id'])
        
        with col2:
            if st.button("🗑️ Delete", key=f"delete_{post['id']}", type="secondary"):
                if st.session_state.get(f"confirm_delete_{post['id']}", False):
                    try:
                        blog_manager.delete_post(post['id'])
                        st.success(f"🗑️ Post '{post['title']}' deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting post: {str(e)}")
                else:
                    st.session_state[f"confirm_delete_{post['id']}"] = True
                    st.warning("⚠️ Click delete again to confirm.")
                    st.rerun()
    
    # Back to home button
    if st.button("← Back to Home", type="secondary"):
        navigate_to("home")

def show_view_page():
    """Display individual post page"""
    if not st.session_state.current_post_id:
        st.error("❌ No post selected.")
        if st.button("← Back to Home", type="secondary"):
            navigate_to("home")
        return
    
    post = blog_manager.get_post(st.session_state.current_post_id)
    if not post:
        st.error("❌ Post not found.")
        if st.button("← Back to Home", type="secondary"):
            navigate_to("home")
        return
    
    # Enhanced post display
    from utils import count_reading_time
    reading_time = count_reading_time(post['content'])
    likes_count = post.get('likes', 0)
    
    st.markdown(f"""
    <div class="post-container" style="margin-bottom: 2rem;">
        <div class="post-title" style="font-size: 2rem; margin-bottom: 1rem;">{post['title']}</div>
        <div class="post-meta" style="margin-bottom: 2rem;">
            👤 <strong>{post['author']}</strong> | 
            📅 {format_date(post['created_at'])} | 
            ⏱️ {reading_time} min read | 
            ❤️ {likes_count} likes
        </div>
        {f'<div class="post-meta" style="margin-bottom: 2rem;">📝 <em>Last Updated: {format_date(post["updated_at"])}</em></div>' if post['updated_at'] else ''}
        <div class="post-content" style="font-size: 1.1rem; line-height: 1.8;">
            {post['content'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation and interaction buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Home", type="secondary"):
            navigate_to("home")
    with col2:
        # Like button
        like_icon = "❤️" if post['id'] in st.session_state.liked_posts else "🤍"
        if st.button(f"{like_icon} Like ({likes_count})", type="secondary"):
            if post['id'] in st.session_state.liked_posts:
                blog_manager.unlike_post(post['id'])
                st.session_state.liked_posts.remove(post['id'])
            else:
                blog_manager.like_post(post['id'])
                st.session_state.liked_posts.add(post['id'])
            st.rerun()
    with col3:
        if st.button("✏️ Edit Post", type="primary"):
            navigate_to("edit", post['id'])

if __name__ == "__main__":
    main()
