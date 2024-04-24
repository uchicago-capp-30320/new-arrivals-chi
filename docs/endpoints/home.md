# Home Page Endpoint Documentation

The home page is the main entry point for users, providing options to access various resources and perform specific tasks, such as toggling languages, reporting bugs, or logging in. It includes buttons that lead to other key sections like general information, legal resources, health resources, organization login, and admin login.

The documentation is divided into 2 sections:
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
This section describes where the home page buttons link to and the corresponding endpoints. It provides an overview of user navigation from the home page.

- [**General Information**:](general_info.md) This button links to the general information page.
  - **Link**: `/general-info`
  - **Endpoint**: `GET /general-info`
  - **Description**: Retrieves static content about Chicago and its resources for new arrivals including how to ride the bus, register for school, and get a CityKey ID.

- [**Legal Resources**:](legal.md) This button links to the legal resources page.
  - **Link**: `/legal-resources`
  - **Endpoint**: `GET /legal-resources`
  - **Description**: Retrieves content for the legal resources page, which guides users through a flowchart to help them find appropriate legal resources based on their situation and legal status.

- [**Health Resources**:](health.md) This button links to the health resources page.
  - **Link**: `/health-resources`
  - **Endpoint**: `GET /health-resources`
  - **Description**: Retrieves general information about heath services, as well as a filterable table of service providers

- **Report a Bug**: This button allows users to submit a bug report.
  - **Link**: `/report-bug`
  - **Endpoint**: `POST /app/bugs/report`
  - **Description**: Submit a bug report with a description of the issue.

- [**Organization Login**:](organization.md) This button allows organizations to log in.
  - **Link**: `/organization-login`
  - **Endpoint**: `POST /app/auth/organization-login`
  - **Description**: Authenticate organization users to access their profiles.

- [**Admin Login**:](admin.md) This button allows administrators to log in.
  - **Link**: `/admin-login`
  - **Endpoint**: `POST /app/auth/admin-login`
  - **Description**: Authenticate administrators to access admin-related features.

- **Toggle Language**: This button toggles the website's language between English and Spanish.
  - **Link**: `/toggle-language`
  - **Endpoint**: `POST /app/settings/language`
  - **Description**: Toggle the website's language.
