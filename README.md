
# Blogify : A Simple Blog Application

A simple blog application built using Django and Django REST Framework. The application provides API endpoints for creating, retrieving, updating, and deleting blog posts, with pagination support for listing posts.
Additionally, the application features a web interface for displaying a list of posts and detailing individual posts.

## Installation
### Prerequisites

Ensure you have the following installed on your machine:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/tanmay031/blogify.git
cd blogify
```

### Step 2: Build and Run the Services

In the project directory, run the following command to build the Docker images and start the services:

```bash
sudo docker-compose up --build
```

This command will:
- Build the Docker images defined in the `Dockerfile`.
- Start the web and database services specified in the `docker-compose.yml` file.

### Step 3: Set Up the Database

Once the services are running, open a new terminal window and run the following commands:

1. **Migrate the Database**:
   ```bash
   sudo docker-compose run web python manage.py migrate
   ```

### Step 4: Create a Superuser

To access the Django admin panel, create a superuser account by running:

```bash
sudo docker-compose run web python manage.py createsuperuser
```

Follow the prompts to set up the superuser credentials.

### Step 5: Access the Application


After completing the above steps, you can access the application as follows:

- **Django Admin Interface**: 
  - Open your web browser and navigate to <a href="http://127.0.0.1:8000/admin/" target="_blank">http://127.0.0.1:8000/admin/</a> to access the Django admin interface.
  - Log in using the superuser credentials you created.

- **Blog Page**: 
  - To view the blog posts, navigate to <a href="http://127.0.0.1:8000/" target="_blank">http://127.0.0.1:8000/</a>.


### Step 6: (Optional) Run Tests

If you have tests configured, you can run them using:

```bash
sudo docker-compose run web python manage.py test posts.tests
```

This command will build the test environment and run your tests.

## API Endpoints

### 1. List All Posts
- **Endpoint:** `GET /api/posts/`
- **Description:** Returns a paginated list of all posts. If `page` and `per_page` parameters are omitted, returns all posts.
- **Parameters:**
  - `page` (optional): The page number to retrieve.
  - `per_page` (optional): The number of posts per page (default is 5, maximum is 15).
- **Example Requests:**
  - **With Pagination:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/api/posts/?page=1&per_page=5"
    ```
  - **Without Pagination:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/api/posts/"
    ```
    This request returns all posts without any pagination.


### 2. Create a New Post
- **Endpoint:** `POST /api/posts/`
- **Description:** Creates a new blog post.
- **Example Request:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/api/posts/"   -H "Content-Type: application/json"   -d '{"title": "Sample Post", "content": "This is a sample blog post."}'
  ```

### 3. Retrieve a Single Post by ID
- **Endpoint:** `GET /api/posts/{id}/`
- **Description:** Retrieves the details of a specific post by its ID.
- **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:8000/api/posts/1/"
  ```

### 4. Update an Existing Post
- **Endpoint:** `PUT /api/posts/{id}/`
- **Description:** Updates the specified post.
- **Example Request:**
  ```bash
  curl -X PUT "http://127.0.0.1:8000/api/posts/1/"   -H "Content-Type: application/json"   -d '{"title": "Updated Post", "content": "Updated content for the blog post."}'
  ```

### 5. Delete a Post
- **Endpoint:** `DELETE /api/posts/{id}/`
- **Description:** Deletes the specified post.
- **Example Request:**
  ```bash
  curl -X DELETE "http://127.0.0.1:8000/api/posts/1/"
  ```

## Pagination
The API uses custom pagination for listing posts:
- **Default Page Size:** 5 posts per page.
- **Maximum Page Size:** 15 posts per page.
- **Query Parameters:** 
  - `page` – Specifies the page number to retrieve.
  - `per_page` – Specifies the number of posts per page.

### Example Pagination Request
Retrieve the second page with 10 posts per page:
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?page=2&per_page=10"
```

### Error Handling for Invalid Page Numbers
If an invalid page number is requested, the API returns a custom error message:
```json
{
  "msg": "Page number is invalid. Please provide a valid page number."
}
```

## Design Decisions
- **Custom Pagination:** Implemented a custom pagination class to empower clients to specify the `per_page` parameter, allowing them to control the number of posts displayed on each page. This feature enhances user experience by providing flexibility in content consumption.
- **REST Framework:** Utilized Django REST Framework's `ModelViewSet` to simplify the implementation of CRUD operations.

