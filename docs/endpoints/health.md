# Health Resources Endpoint Documentation

The health resources page provides static information and a filterable table for finding specific health services. The main page includes a two-button approach to direct users to either a filterable table for immediate assistance or a static page with health information.

The documentation is divided into three main sections:
- [Retrieve Health Resources Page Content](#retrieve-health-resources-page-content)
- [Using the Filterable Table](#using-the-filterable-table)
- [Health Page Buttons and Links](#health-page-buttons-and-links)

## Retrieve Health Resources Page Content
### Get Health Resources Page Content
- **Endpoint**: `GET /app/health`
- **Description**: Retrieve a page with static information and two buttons: one for immediate assistance (leading to a filterable table) and one for learning more about health resources.
- **Responses**:
  - `200 OK`: Health resources content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "content": "Welcome to the Health Resources page. Here, you'll find information on healthcare facilities, free clinics, and other resources for new members of the Chicago community.",
    "buttons": [
      {
        "name": "I need assistance immediately",
        "link": "/app/health-search"
      },
      {
        "name": "I want to learn more about health and medical resources",
        "link": "/app/health-info"
      },
      {
        "name": "Home",
        "link": "/home"
      }
    ]
  }
  ```

### Static Page with Information on Health Resources
Users can navigate to a static page for additional information about health and medical resources.

- **Endpoint**: `GET /app/health-info`
- **Description**: Retrieve a static page with information about available health resources for new migrants, including health clinics, emergency services, and other medical facilities.
- **Responses**:
  - `200 OK`: Information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

## Using the Filterable Table
Users can navigate to the filterable table for immediate assistance by clicking the "I need assistance immediately" button. The table supports filtering based on criteria like services, neighborhood, organization, operating hours, and status (e.g., asylum, undocumented, etc.). Each entry's organization name in the filterable table links to the organization's page, allowing users to find more information about the organization.

- **Endpoint**: `GET /app/health-search`
- **Description**: Retrieve a filterable table of health services with various filter options.
- **Query Parameters**:
  - `services`: Filter by specific services (e.g., "medical", "dental").
  - `neighborhood`: Filter by location or neighborhood.
  - `organization`: Filter by organization name.
  - `hours`: Filter by operating hours (e.g., "9am - 5pm").
  - `status`: Filter by asylum, undocumented, etc.
- **Responses**:
  - `200 OK`: Table content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "table": [
      {
        "organization": "Health Center A",
        "neighborhood": "North Side",
        "services": ["Medical Checkups", "Vaccinations"],
        "hours": "9am - 5pm",
        "organization_link": "/app/organization/health-center-a",
        "address_link": "https://maps.google.com/?q=123+Main+St,+Chicago"
      },
      {
        "organization": "Health Center B",
        "neighborhood": "South Side",
        "services": ["Emergency Services"],
        "hours": "10am - 6pm",
        "organization_link": "/app/organization/health-center-b",
        "address_link": "https://maps.google.com/?q=456+Elm+St,+Chicago"
      }
    ],
    "buttons": [
      {
        "name": "Return to Home Page",
        "link": "/home"
      }
    ]
  }
  ```

## Health Page Buttons and Links
This section describes the buttons and links on the health resources page.

### Search Health Services
- **Endpoint**: `GET /app/health-search`
- **Description**: This button leads to a filterable table of health services based on various criteria.

### Learn More About Health Resources
- **Endpoint**: `GET /app/health-info`
- **Description**: This button leads to a static page with general information about health resources.

### Return to Home Page
- **Endpoint**: `GET /app/home`
- **Description**: Button to navigate back to the home page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
