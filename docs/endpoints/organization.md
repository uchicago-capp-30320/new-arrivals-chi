# Organization Endpoint Documentation

The organization page allows community organizations to manage their profiles, update their resources and services, and perform various tasks with their accounts. It includes buttons that lead to specific actions, such as profile updates, account setup, and deletion, along with a logout option.

The documentation is divided into four sections:
- [Organization Login](#organization-login)
- [Organization Page Content](#organization-page-content)
- [Organization Setup](#organization-setup)
- [Organization Page Buttons and Links](#organization-page-buttons-and-links)

## Organization Login
### Authenticate Organization
- **Endpoint**: `POST /app/auth/organization-login`
- **Description**: Log in to the organization page with credentials.
- **Request Body**:
  - `username`: Organization's username.
  - `password`: Organization's password.
- **Responses**:
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "username": "org123",
    "password": "mypassword"
  }
  ```

## Organization Page Content
### Get Organization Profile
- **Endpoint**: `GET /app/organization/profile`
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
- **Endpoint**: `PUT /app/organization/profile`
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

### Delete Organization Account
- **Endpoint**: `DELETE /app/organization/profile`
- **Description**: Delete the logged-in organization's account.
- **Responses**:
  - `200 OK`: Account deleted successfully.
  - `401 Unauthorized`: Unauthorized action.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "message": "Organization account deleted successfully."
  }
  ```

## Organization Setup
Organizations can set up new accounts via a direct link, creating a username, password, and other profile information.

### Create Organization Account
- **Endpoint**: `POST /app/organization/setup`
- **Description**: Set up a new organization account through a direct link.
- **Request Body**:
  - `username`, `password`, and other profile details (`address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Responses**:
  - `200 OK`: Account created successfully.
  - `400 Bad Request`: Incorrect input data.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "username": "org124",
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

- **Return to Home Page**: This button allows users to return to the home page.
  - **Link**: `/home`
  - **Endpoint**: `GET /app/home`
  - **Description**: Go back to the home page from the organization page.

- **Logout**: This button allows users to log out of the organization page.
  - **Link**: `/app/auth/org-logout`
  - **Endpoint**: `POST /app/auth/org-logout`
  - **Description**: Log out and end the current session.
  - **Responses**:
    - `200 OK`: Logout successful.
    - `401 Unauthorized`: Unauthorized access attempt.
    - `500 Internal Server Error`: Indicates a server error.
