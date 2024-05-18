# Admin Page Endpoint Documentation

The admin page provides administrative functions for managing organizations and other system-wide tasks. Access is restricted to users with admin credentials. This documentation covers admin-related operations, including setting up organization accounts, sending temporary passwords, and providing links to reset passwords.

The documentation is divided into the following sections:
- [Admin Login](#admin-login)
- [Retrieve Admin Page](#retrieve-admin-page)
- [Set Up and Update a New Organization](#set-up-and-update-a-new-organization)
- [Admin Password Reset](#admin-password-reset)
- [Admin Page Buttons and Links](#admin-page-buttons-and-links)

## Admin Login
### Authenticate Admin
- **Endpoint**: `POST /login`
- **Description**: Log in to the admin page with admin credentials.
- **Request Body**:
  - `email`: Admin's email.
  - `password`: Admin's password.
- **Responses**:
  - `200 OK`: Login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.

## Retrieve Admin Page
### Get Admin Page Content
- **Endpoint**: `GET /dashboard`
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
        "link": "/"
      },
      {
        "name": "Logout",
        "link": "/auth/admin-logout"
      }
    ]
  }
  ```

### Change Organization Status from Admin Dashboard
- **Endpoint**: `POST /status`
- **Description**: Update organization status to VISIBLE, INVISIBLE, or SUSPEND.
- **Responses**:
  - `200 OK`: Organization status updated successfully.
  - `401 Unauthorized`: Unauthorized action.
  - `500 Internal Server Error`: Indicates a server error.

## Set Up and Update a New Organization

### Create Organization Account
- **Endpoint**: `POST /add_organization`
- **Description**: Admins add a new organization with required information like username (email), temporary password, and other profile details. An email is sent with a temporary password and a link for the organization to reset their password.
- **Responses**:
  - `200 OK`: Organization created successfully.
  - `400 Bad Request`: Invalid data provided.
  - `500 Internal Server Error`: Indicates a server error.

### Edit Organization Info
- **Endpoint**: `POST /edit_organization`
- **Description**: Update the organization's profile information.
- **Request Body**:
  - `new_password`: The new password to be set.
  - `confirm_password`: Confirmation of the new password.
- **Responses**:
  - `200 OK`: Organization profile updated successfully.
  - `400 Bad Request`: Invalid password mismatch, or other validation error.
  - `500 Internal Server Error`: Indicates a server error.

## Admin Password Reset

### Change Password
- **Endpoint**: `POST /change_password`
- **Description**: Request a password reset email for an admin user.
- **Request Body**:
  - `email`: Email
  - `old_password`: Old password
- **Responses**:
  - `200 OK`: Password change successful
  - `400 Bad Request`: Invalid email or missing required information.
  - `500 Internal Server Error`: Indicates a server error.

## Admin Page Buttons and Links
### Return to Home Page
- **Endpoint**: `GET /`
- **Description**: Button to navigate back to the home page from the admin page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Admin Logout
- **Endpoint**: `POST /logout`
- **Description**: Logs out the admin and ends the session.
- **Implementation**:
  - The `href="url_for('auth.logout')"` value in the HTML template points to this endpoint to trigger logout functionality.
- **Responses**:
  - `200 OK`: Logout successful.
  - `401 Unauthorized`: Unauthorized action.
  - `500 Internal Server Error`: Server error.
