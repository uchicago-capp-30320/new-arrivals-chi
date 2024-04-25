# Home Page Endpoint Documentation

The home page is the main entry point for users, providing options to access various resources and perform specific tasks, such as toggling languages, reporting bugs, or logging in. It includes buttons that lead to key sections like general information, legal resources, health resources, organization login, and admin login.

The documentation is divided into two sections:
- [Retrieve Home Page Content](#retrieve-home-page-content)
- [Home Page Buttons and Links](#home-page-buttons-and-links)

## Retrieve Home Page Content
### Get Home Page Content
- **Endpoint**: `GET /app/home`
- **Description**: Retrieve the content for the home page, which includes sections for general information, legal resources, and health resources, along with action buttons for logging in, reporting bugs, and toggling languages.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "sections": [
      {
        "name": "General Information",
        "link": "/general-info"
      },
      {
        "name": "Legal Resources",
        "link": "/legal-resources"
      },
      {
        "name": "Health Resources",
        "link": "/health-resources"
      }
    ],
    "actions": [
      {
        "name": "Report a Bug",
        "link": "/report-bug"
      },
      {
        "name": "Organization Login",
        "link": "/organization-login"
      },
      {
        "name": "Admin Login",
        "link": "/admin-login"
      },
      {
        "name": "Toggle Language",
        "link": "/toggle-language"
      }
    ]
  }
  ```

## Home Page Buttons and Links
This section describes where the home page buttons link to and the corresponding endpoints, providing an overview of user navigation from the home page.

### General Information
- **Endpoint**: `GET /general-info`
- **Description**: This button links to the general information page. It provides static content about Chicago and its resources for new arrivals, including how to ride the bus, register for school, and get a CityKey ID.
- **Responses**:
  - `200 OK`: Content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Legal Resources
- **Endpoint**: `GET /legal-resources`
- **Description**: This button links to the legal resources page. It retrieves content for the legal resources page, which guides users through a flowchart to help them find appropriate legal resources based on their situation and legal status.
- **Responses**:
  - `200 OK`: Legal resources content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Health Resources
- **Endpoint**: `GET /health-resources`
- **Description**: This button links to the health resources page. It provides general information about health services, as well as a filterable table of service providers.
- **Responses**:
  - `200 OK`: Health resources content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Report a Bug
- **Endpoint**: `POST /app/bugs/report`
- **Description**: This button allows users to submit a bug report with a description of the issue.
- **Responses**:
  - `200 OK`: Bug report submitted successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Organization Login
- **Endpoint**: `POST /app/auth/organization-login`
- **Description**: This button allows organizations to log in. It authenticates organization users to access their profiles.
- **Responses**:
  - `200 OK`: Organization login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.

### Admin Login
- **Endpoint**: `POST /app/auth/admin-login`
- **Description**: This button allows administrators to log in. It authenticates admin users to access admin-related features.
- **Responses**:
  - `200 OK`: Admin login successful.
  - `401 Unauthorized`: Invalid credentials.
  - `500 Internal Server Error`: Indicates a server error.

### Toggle Language
- **Endpoint**: `POST /app/settings/language`
- **Description**: This button toggles the website's language between English and Spanish.
- **Responses**:
  - `200 OK`: Language toggled successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Return to Home Page
- **Endpoint**: `GET /app/home`
- **Description**: This button allows users to return to the home page from other sections.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
