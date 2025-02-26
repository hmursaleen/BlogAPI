# Blogging Platform API

## Overview
This is a RESTful API for a blogging platform built using Django and MongoDB. The API allows users to create, read, update, and delete blog posts, manage comments, search for blog posts, and receive notifications. The project follows best practices and principles such as SOLID and DRY, and implements efficient system design.

This project is inspired by the [Roadmap Blogging Platform API Challenge](https://roadmap.sh/projects/blogging-platform-api).

## Features
- User authentication with JWT
- Blog post creation, update, delete, and retrieval
- Comment management system
- Full-text search functionality
- Real-time notifications using Redis
- Load testing with Locust
- Performance optimization with MongoDB indexing
- API documentation using drf-yasg

## Technologies Used
- **Backend:** Django, Django REST Framework (DRF)
- **Database:** MongoDB (using PyMongo as the connector)
- **Search & Caching:** Redis
- **Asynchronous Tasks:** Celery
- **Testing:** Unit tests with Django's TestCase, Load Testing with Locust
- **Documentation:** drf-yasg
- **Containerization:** Docker (for MongoDB and Redis)

## Installation & Setup
### Prerequisites
- Python 3.10+
- Docker
- MongoDB (running in Docker)
- Redis (running in Docker)

### Clone the Repository
```bash
 git clone https://github.com/yourusername/blogging-platform-api.git
 cd blogging-platform-api
```

### Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file and add:
```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=blog_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
DEBUG=True
```

### Start MongoDB and Redis with Docker
```bash
docker-compose up -d
```

### Apply Migrations
```bash
python manage.py migrate
```

### Run the Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
#### Register a User
**Endpoint:** `POST /api/auth/register/`
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
}
```

#### Login
**Endpoint:** `POST /api/auth/login/`
```json
{
    "username": "testuser",
    "password": "securepassword"
}
```

#### Logout
**Endpoint:** `POST /api/auth/logout/`

### Blog Posts
#### Create a Post (Authenticated Users Only)
**Endpoint:** `POST /api/posts/`
```json
{
    "title": "My First Blog Post",
    "content": "This is my first blog post.",
    "tags": ["django", "mongodb"]
}
```

#### Get a Post
**Endpoint:** `GET /api/posts/{post_id}/`

#### Update a Post (Author Only)
**Endpoint:** `PUT /api/posts/{post_id}/`
```json
{
    "title": "Updated Title",
    "content": "Updated Content"
}
```

#### Delete a Post (Author Only)
**Endpoint:** `DELETE /api/posts/{post_id}/`

### Comments
#### Add a Comment
**Endpoint:** `POST /api/posts/{post_id}/comments/`
```json
{
    "content": "This is a great post!"
}
```

#### Get Comments for a Post
**Endpoint:** `GET /api/posts/{post_id}/comments/`

### Search
#### Search for Posts
**Endpoint:** `GET /api/posts/?search=django`

### Notifications
#### Get Notifications
**Endpoint:** `GET /api/notifications/`

## Load Testing
Locust was used for performance testing. To run Locust:
```bash
locust -f locustfile.py
```
Navigate to `http://localhost:8089` to run tests.

## API Documentation
API documentation is generated using drf-yasg. After running the server, open the following:
- **Swagger UI:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Indexing for Performance Optimization
To improve database query performance, indexes were added to frequently queried fields:
```python
self.collection.create_index([("title", ASCENDING)], name="idx_title")
self.collection.create_index([("created_at", DESCENDING)], name="idx_created_at")
self.collection.create_index([("tags", ASCENDING)], name="idx_tags")
```
Indexes can also be created manually using:
```bash
python manage.py create_indexes
```

## Running Tests
To run unit tests:
```bash
python manage.py test
```

## Contribution
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first.

## License
This project is open-source and available under the MIT License.