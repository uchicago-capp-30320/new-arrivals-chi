# Organization Endpoint Documentation

The organization page allows community organizations to manage their profiles, update their resources and services, and perform various tasks with their accounts. It includes buttons that lead to specific actions, such as profile updates, account setup, and deletion, along with a logout option.

The documentation is divided into the following sections:
- [Organization Login](#organization-login)
- [Organization Page Content](#organization-page-content)
- [Organization Setup](#organization-setup)
- [Organization Page Buttons and Links](#organization-page-buttons-and-links)

## Organization Login
### Authenticate Organization
- **Endpoint**: `POST /login`
- **Description**: Log in to the organization page with credentials.
- **Request Body**:
  - `email`: Organization's email.
  - `password`: Organization's password.
- **Responses**:
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "email": "org123@email.com",
    "password": "mypassword"
  }
  ```

## Organization Page Content
### Get Organization Profile
- **Endpoint**: `GET /profile`
- **Description**: Retrieve the profile information of the logged-in organization.
- **Responses**:
  - `200 OK`: Profile information retrieved successfully.
  - `401 Unauthorized`: Unauthorized access attempt.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "address": "123 Main St, Chicago",
    "phone": "123-456-7890",
    "hours": "9am - 5pm",
    "languages": ["English", "Spanish"],
    "supplies": ["food", "clothes"],
    "services": ["legal aid", "medical attention"]
  }
  ```

### Update Organization Profile
- **Endpoint**: `POST /update_profile`
- **Description**: Update the organization's profile information.
- **Request Body**:
  - Profile details to update (e.g., `address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Responses**:
  - `200 OK`: Profile updated successfully.
  - `400 Bad Request`: Incorrect input data.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "address": "123 Main St, Chicago",
    "phone": "123-456-7890",
    "hours": "9am - 5pm",
    "languages": ["English", "Spanish"],
    "supplies": ["food", "clothes"],
    "services": ["legal aid", "medical attention"]
  }
  ```

### Suspend Organization Account
- **Endpoint**: `POST /organization/suspend`
- **Description**: Suspend the organization's account by updating the active status to inactive.
- **Responses**:
  - `200 OK`: Account suspended successfully.
  - `401 Unauthorized`: Unauthorized action.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "message": "Organization account suspended successfully."
  }
  ```

## Organization Setup
Organizations can set up new accounts via a direct link, creating a username (email), password, and other profile information.

### Create Organization Account
- **Endpoint**: `POST /organization/setup`
- **Description**: Set up a new organization account through a direct link.
- **Request Body**:
  - `email`, `password`, and other profile details (`address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Responses**:
  - `200 OK`: Account created successfully.
  - `400 Bad Request`: Incorrect input data.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "email": "org124@email.com",
    "password": "mypassword",
    "address": "123 Main St, Chicago",
    "phone": "123-456-7890",
    "hours": "9am - 5pm",
    "languages": ["English", "Spanish"],
    "supplies": ["food", "clothes"],
    "services": ["legal aid", "medical attention"]
  }
  ```

## Organization Page Buttons and Links
This section describes the buttons and links on the organization page, providing navigation options and other common actions.

### Return to Home Page
- **Endpoint**: ``GET /`
- **Description**:   Button to navigate back to the home page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Org Logout
- **Endpoint**: `POST /auth/org-logout`
- **Description**: Logs out the admin and ends the session.
- **Implementation**:
  - The `href="url_for('auth.logout')"` value in the HTML template points to this endpoint to trigger logout functionality.
- **Responses**:
  - `200 OK`: Logout successful.
  - `401 Unauthorized`: Unauthorized action.
  - `500 Internal Server Error`: Server error.
