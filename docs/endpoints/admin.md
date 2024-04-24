# Admin Page Endpoint Documentation

The admin page provides administrative functions for managing organizations and other system-wide tasks. Access is restricted to users with admin credentials.

The documentation is divided into 3 sections:
- [Admin Login](#admin-login)
- [Get Admin Page Content](#get-admin-page-content)
- [Admin Page Buttons and Links](#admin-page-buttons-and-links)

## Admin Login
### Authenticate Admin
- **Endpoint**: `POST /app/auth/admin-login`
- **Description**: Log in to the admin page with credentials.
- **Request Body**:
  - `username`: Admin's username.
  - `password`: Admin's password.
- **Responses**:
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "username": "admin123",
    "password": "adm!np@ssword"
  }

## Get Admin Page Content
- **Endpoint**: `GET /app/admin/dashboard`
- **Description**: Retrieve the admin dashboard content, which includes an overview of organizations and admin-related tasks.
- **Responses**:
  - `200 OK`: Admin page content retrieved successfully.
  - `401 Unauthorized`: Unauthorized access attempt.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "organizations": [
      {
        "name": "org123",
        "address": "123 Main St, Chicago",
        "phone": "123-456-7890",
        "hours": "9am - 5pm",
        "languages": ["English", "Spanish"],
        "supplies": ["food", "clothes"],
        "services": ["legal aid", "medical attention"]
      }
    ],
    "adminTasks": [
      {
        "name": "Add Organization",
        "link": "/admin/add-organization"
      },
      {
        "name": "Edit Organization",
        "link": "/admin/edit-organization"
      },
      {
        "name": "Delete Organization",
        "link": "/admin/delete-organization"
      }
    ],
    "otherActions": [
      {
        "name": "Home Page",
        "link": "/home"
      },
      {
        "name": "Logout",
        "link": "/app/auth/admin-logout"
      }
    ]
  }
  ```

## Admin Page Buttons and Links
This section describes where the admin page buttons lead to and the corresponding endpoints, providing an overview of available actions for administrators.

- **Add Organization**: Allows admins to add a new organization.
  - **Link**: `/admin/add-organization`
  - **Endpoint**: `POST /app/admin/organization`
  - **Description**: Add a new organization with required information like username, password, and other profile details.

- **Edit Organization**: Allows admins to edit an existing organization.
  - **Link**: `/admin/edit-organization`
  - **Endpoint**: `POST /app/admin/organization`
  - **Description**: Update an organization's profile details.

- **Delete Organization**: Allows admins to delete an organization by username.
  - **Link**: `/admin/delete-organization`
  - **Endpoint**: `DELETE /app/admin/organization/{username}`
  - **Description**: Delete an organization by its username. The `{username}` parameter specifies the organization to be deleted.
  - **Responses**:
    - `200 OK`: Organization deleted successfully.
    - `404 Not Found`: Organization not found.
    - `401 Unauthorized`: Unauthorized action.

- **Home Page**: Provides a button to return to the home page.
  - **Link**: `/home`
  - **Endpoint**: `GET /app/home`
  - **Description**: Returns to the home page.

- **Logout**: Allows admins to log out of the admin session.
  - **Link**: `/app/auth/admin-logout`
  - **Endpoint**: `POST /app/auth/admin-logout`
  - **Description**: Log out and invalidate the current authentication token.
  - **Responses**:
    - `200 OK`: Logout successful.
    - `401 Unauthorized`: Unauthorized access.
