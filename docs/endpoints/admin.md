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

## Organization Password Setup 
The process for organizations to set up or reset their passwords involves sending a temporary password via email and providing a link to reset it. This documentation outlines the key endpoints for these operations.

### Send Email with Temporary Password and Reset Link
- **Endpoint**: `POST /app/admin/org-email`
- **Description**: Admins send an email with a temporary password and a link for the organization to reset their password.
- **Request Body**:
  - `email`: The email address to send the temporary password and reset link.
- **Responses**:
  - `200 OK`: Email sent successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Validate Organization Reset Token
- **Endpoint**: `GET /app/auth/validate-org-reset-token`
- **Description**: Validates the token from the email to ensure it's valid for resetting the organization's password.
- **Query Parameters**:
  - `token`: The unique token from the reset email.
- **Responses**:
  - `200 OK`: Token validated successfully.
  - `400 Bad Request`: Invalid or expired token.
  - `500 Internal Server Error`: Indicates a server error.

### Set New Organization Password
- **Endpoint**: `POST /app/auth/org-set-password`
- **Description**: Set a new password for the organization account after validating the token.
- **Request Body**:
  - `token`: The unique token from the reset email.
  - `new_password`: The new password to be set.
  - `confirm_password`: Confirmation of the new password.
- **Responses**:
  - `200 OK`: Password reset successfully.
  - `400 Bad Request`: Invalid token, password mismatch, or other validation error.
  - `500 Internal Server Error`: Indicates a server error.


## Update Organization Information
### Edit Organization
- **Endpoint**: `POST /app/admin/organization`
- **Description**: Update an existing organization's profile details.
- **Responses**:
  - `200 OK`: Organization updated successfully.
  - `400 Bad Request`: Incorrect data provided.
  - `500 Internal Server Error`: Indicates a server error.

### Suspend Organization
- **Endpoint**: `POST /app/admin/organization/{username}`
- **Description**: Suspend an organization's account by updating its status to inactive.
- **Responses**:
  - `200 OK`: Organization suspended successfully.
  - `404 Not Found`: Organization not found.
  - `401 Unauthorized`: Unauthorized action.

## Admin Password Reset 
The admin password reset process consists of endpoints that trigger a password reset email, validate the reset token, and set the new password. This documentation outlines the key endpoints involved in the process.

### Request Password Reset
- **Endpoint**: `POST /app/auth/admin-reset-password`
- **Description**: Request a password reset email for an admin user.
- **Request Body**:
  - `email`: The admin's registered email address.
- **Responses**:
  - `200 OK`: Password reset email sent successfully.
  - `400 Bad Request`: Invalid email or missing required information.
  - `500 Internal Server Error`: Indicates a server error.

### Validate Reset Token
- **Endpoint**: `GET /app/auth/admin-validate-reset-token`
- **Description**: Validates the token from the password reset email to ensure it's correct and hasn't expired.
- **Query Parameters**:
  - `token`: The unique token from the reset email.
- **Responses**:
  - `200 OK`: Token validated successfully.
  - `400 Bad Request`: Invalid or expired token.
  - `500 Internal Server Error`: Indicates a server error.

### Set New Password
- **Endpoint**: `POST /app/auth/admin-set-new-password`
- **Description**: Set a new password for the admin account after the token has been validated.
- **Request Body**:
  - `token`: The unique token from the reset email.
  - `new_password`: The new password to be set.
  - `confirm_password`: Confirmation of the new password.
- **Responses**:
  - `200 OK`: Password reset successfully.
  - `400 Bad Request`: Invalid token, password mismatch, or other validation error.
  - `500 Internal Server Error`: Indicates a server error.


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
