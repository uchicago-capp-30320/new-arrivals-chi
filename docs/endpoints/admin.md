# Admin Page Endpoint Documentation

The admin page provides administrative functions for managing organizations and other system-wide tasks. Access is restricted to users with admin credentials. This documentation covers admin-related operations, including setting up organization accounts, sending temporary passwords, and providing links to reset passwords.

The documentation is divided into the following sections:
- [Admin Login](#admin-login)
- [Retrieve Admin Page](#retrieve-admin-page)
- [Set Up a New Organization](#set-up-a-new-organization)
- [Update Organization Information](#update-organization-information)
- [Admin Page Buttons and Links](#admin-page-buttons-and-links)

## Admin Login
### Authenticate Admin
- **Endpoint**: `POST /app/auth/admin-login`
- **Description**: Log in to the admin page with admin credentials.
- **Request Body**:
  - `username`: Admin's username.
  - `password`: Admin's password.
- **Responses**:
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.

## Retrieve Admin Page
### Get Admin Page Content
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
        "name": "Suspend Organization",
        "link": "/admin/suspend-organization"
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

## Set Up a New Organization
### Create Organization Account
- **Endpoint**: `POST /app/admin/organization`
- **Description**: Admins add a new organization with required information like username, temporary password, and other profile details.
- **Responses**:
  - `200 OK`: Organization created successfully.
  - `400 Bad Request`: Invalid data provided.
  - `500 Internal Server Error`: Indicates a server error.

### Send Email with Temporary Password and Reset Link
- **Endpoint**: `POST /app/admin/email`
- **Description**: Admins send an email with a temporary password and a link for the organization to reset their password.
- **Responses**:
  - `200 OK`: Email sent successfully.
  - `500 Internal Server Error`: Indicates a server error.

## Update Organization Information
### Edit Organization
- **Endpoint**: `PUT /app/admin/organization`
- **Description**: Update an existing organization's profile details.
- **Responses**:
  - `200 OK`: Organization updated successfully.
  - `400 Bad Request`: Incorrect data provided.
  - `500 Internal Server Error`: Indicates a server error.

### Suspend Organization
- **Endpoint**: `PUT /app/admin/organization/{username}`
- **Description**: Suspend an organization's account by updating its status to inactive.
- **Responses**:
  - `200 OK`: Organization suspended successfully.
  - `404 Not Found`: Organization not found.
  - `401 Unauthorized`: Unauthorized action.

## Admin Page Buttons and Links

### Return to Home Page
- **Endpoint**: `GET /app/home`
- **Description**: Button to navigate back to the home page from the admin page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Logout
- **Endpoint**: `POST /app/auth/admin-logout`
- **Description**: Log out and end the current admin session.
- **Responses**:
  - `200 OK`: Logout successful.
  - `401 Unauthorized`: Unauthorized action.
