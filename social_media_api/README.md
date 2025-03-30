# Social Media API Documentation

## Base URL
All endpoints are prefixed by the base URL of your deployed application.  
**Example**: If your domain is `https://api.example.com`, all endpoints are relative to that domain.

---

## Endpoints

### 1. Accounts Endpoints

#### User Registration
- **URL**: `/register/`  
- **Method**: `POST`  
- **Description**: Create a new user account.  
- **Request Body Example**:  
  ```json
  {
    "username": "exampleuser",
    "email": "user@example.com",
    "password": "yourpassword",
    "password2": "yourpassword"
  }
  ```

#### User Login
- **URL**: `/login/`  
- **Method**: `POST`  
- **Description**: Authenticate a user and return a token/session.  
- **Request Body Example**:  
  ```json
  {
    "email": "youremail",
    "password": "yourpassword"
  }
  ```

#### User Profile
- **URL**: `/profile/`  
- **Method**: `GET`  
- **Description**: Retrieve details of the authenticated user.

#### Follow User
- **URL**: `/follow/<int:user_id>/`  
- **Method**: `POST`  
- **Description**: Follow the user specified by `user_id`.  
- **Example**: `/follow/5/` (Follows user with ID 5).

#### Unfollow User
- **URL**: `/unfollow/<int:user_id>/`  
- **Method**: `POST`  
- **Description**: Unfollow the user specified by `user_id`.  
- **Example**: `/unfollow/5/` (Unfollows user with ID 5).

---

### 2. Posts and Comments Endpoints

#### Posts
- **List Posts**  
  - **URL**: `/api/posts/`  
  - **Method**: `GET`  
  - **Description**: Retrieve all posts.

- **Create Post**  
  - **URL**: `/api/posts/`  
  - **Method**: `POST`  
  - **Description**: Create a new post.  
  - **Request Body Example**:  
    ```json
    {
      "title": "Post Title",
      "content": "Post content goes here."
    }
    ```  
  - **Note**: Authenticated user is automatically set as the author.

- **Retrieve Post**  
  - **URL**: `/api/posts/<int:pk>/`  
  - **Method**: `GET`  
  - **Description**: Get details of a specific post.

- **Update Post**  
  - **URL**: `/api/posts/<int:pk>/`  
  - **Method**: `PUT`/`PATCH`  
  - **Description**: Update a post (owner only).

- **Delete Post**  
  - **URL**: `/api/posts/<int:pk>/`  
  - **Method**: `DELETE`  
  - **Description**: Delete a post (owner only).

#### Comments
- **List Comments**  
  - **URL**: `/api/comments/`  
  - **Method**: `GET`  
  - **Description**: Retrieve all comments.

- **Create Comment**  
  - **URL**: `/api/comments/`  
  - **Method**: `POST`  
  - **Description**: Create a new comment.  
  - **Request Body Example**:  
    ```json
    {
      "post": 1,
      "content": "This is a comment."
    }
    ```  
  - **Note**: 
    - Authenticated user is set as the comment author.  
    - Generates a notification for the post author.

- **Retrieve Comment**  
  - **URL**: `/api/comments/<int:pk>/`  
  - **Method**: `GET`  
  - **Description**: Get details of a specific comment.

- **Update Comment**  
  - **URL**: `/api/comments/<int:pk>/`  
  - **Method**: `PUT`/`PATCH`  
  - **Description**: Update a comment (owner only).

- **Delete Comment**  
  - **URL**: `/api/comments/<int:pk>/`  
  - **Method**: `DELETE`  
  - **Description**: Delete a comment (owner only).

---

### 3. Feed
- **User Feed**  
  - **URL**: `/api/feed/`  
  - **Method**: `GET`  
  - **Description**: Get posts from followed users (sorted by most recent).

---

### 4. Post Like/Unlike

#### Like a Post
- **URL**: `/api/posts/<int:pk>/like/`  
- **Method**: `POST`  
- **Description**: Like a post.  
- **Notes**:  
  - Returns `400 Bad Request` if already liked.  
  - Generates a notification for the post author.

#### Unlike a Post
- **URL**: `/api/posts/<int:pk>/unlike/`  
- **Method**: `POST`  
- **Description**: Remove a like.  
- **Notes**:  
  - Returns `400 Bad Request` if not already liked.

---

### 5. Notifications

#### List Notifications
- **URL**: `/notifications/`  
- **Method**: `GET`  
- **Description**: Retrieve user notifications (sorted by latest, unread highlighted).

#### Mark Notification as Read
- **URL**: `/notifications/<int:pk>/`  
- **Method**: `POST`/`PATCH`  
- **Description**: Mark a notification as read.

---

## Usage Notes

### Authentication
- Most endpoints (except `/register/` and `/login/`) require authentication.

### Error Handling
- `200 OK`: Success (GET, POST for actions like unfollow).  
- `201 Created`: Success (POST for creation).  
- `400 Bad Request`: Invalid request (e.g., duplicate like).

### Notifications
Automatically generated for:  
1. Post likes  
2. Comments  
3. Follows