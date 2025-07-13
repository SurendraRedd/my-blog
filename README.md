# Personal Blog Application

## Overview

This is a personal blog application built with Streamlit that allows users to create, read, and manage blog posts. The application uses a simple file-based storage system with JSON for data persistence and provides a clean web interface for blog management.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### UI/UX Improvements (July 13, 2025)
- Added modern gradient styling with custom CSS
- Enhanced post display with styled containers and cards
- Improved navigation with better button styling
- Added reading time calculation for posts
- Enhanced sidebar with blog statistics
- Improved form styling with better visual hierarchy
- Added word count and reading time displays in forms
- Better pagination controls with improved styling
- Enhanced empty states with informative messages
- Added visual feedback for search results
- Improved post management interface with better card layout

### Feature Additions (July 13, 2025)
- **Dark Mode Support**: Added toggle for dark/light theme with dynamic CSS
- **Like System**: Implemented like/unlike functionality for posts
- **Like Statistics**: Added like counts to posts and total likes in sidebar
- **Enhanced Post Metadata**: Like counts integrated into post displays
- **Session State Management**: Added user-specific like tracking
- **Database Schema Update**: Posts now include likes field with backward compatibility

## System Architecture

The application follows a simple three-tier architecture:

1. **Presentation Layer**: Streamlit-based web interface (`app.py`)
2. **Business Logic Layer**: Blog management operations (`blog_manager.py`)
3. **Data Layer**: JSON file-based storage (`data/blog_posts.json`)

The architecture prioritizes simplicity and ease of deployment, making it suitable for personal use without requiring complex database setup.

## Key Components

### Frontend (app.py)
- **Framework**: Streamlit for web UI
- **Navigation**: Session state-based page navigation system
- **Features**: Home page, post creation, search functionality, pagination
- **State Management**: Uses Streamlit's session state for managing current page, post ID, search queries, and pagination

### Backend (blog_manager.py)
- **Data Operations**: CRUD operations for blog posts
- **Storage**: JSON file-based persistence in `data/` directory
- **Post Structure**: Posts contain ID, title, content, author, creation timestamp, and update timestamp
- **ID Generation**: Uses UUID for unique post identification

### Utilities (utils.py)
- **Date Formatting**: Converts ISO timestamps to human-readable format
- **Content Processing**: Text truncation for post previews
- **Search**: Full-text search across title, content, and author fields
- **Validation**: Input validation for post data

## Data Flow

1. **Post Creation**: User input → validation → BlogManager → JSON storage
2. **Post Retrieval**: JSON file → BlogManager → formatting → Streamlit UI
3. **Search**: User query → search algorithm → filtered results → display
4. **Navigation**: User interaction → session state update → page re-render

## External Dependencies

- **Streamlit**: Web framework for the user interface
- **Python Standard Library**: 
  - `json` for data serialization
  - `datetime` for timestamp management
  - `pathlib` for file system operations
  - `uuid` for unique ID generation
  - `os` for operating system interactions
  - `re` for regular expressions (imported but not actively used)

## Deployment Strategy

- **Local Development**: Direct Python execution with Streamlit
- **File Storage**: Simple JSON file in `data/` directory
- **Scalability**: Currently designed for single-user, low-volume usage
- **Portability**: Self-contained application with minimal dependencies

### Key Architectural Decisions

1. **JSON over Database**: Chosen for simplicity and zero-configuration deployment, suitable for personal blogs with moderate content volume
2. **Streamlit Framework**: Selected for rapid development and built-in UI components, eliminating need for separate frontend development
3. **Session State Navigation**: Implements client-side navigation without URL routing, maintaining simplicity while providing smooth user experience
4. **UUID Post IDs**: Ensures unique identification without requiring database auto-increment functionality
5. **File-based Storage**: Eliminates database setup complexity, making the application immediately deployable

### Current Limitations

- No user authentication system
- Single-user design
- No data backup or recovery mechanisms
- Limited scalability for large numbers of posts
- No rich text editing capabilities
- No comment system or user interactions

The application is designed as a simple, personal blogging solution that prioritizes ease of use and deployment over advanced features.