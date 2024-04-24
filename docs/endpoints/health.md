# Health Resources Endpoint Documentation

The health resources page provides static information and a filterable table to find specific health services.

The documentation is divided into 3 sections:
- [Retrieve Health Resources Information Content](#retrieve-health-resources-information-content)
- [Search Health Services](#search-health-services)
- [Health Page Buttons and Links](#health-page-buttons-and-links)

## Retrieve Health Resources Information Content
### Get Health Resources Page Content
- **Endpoint**: `GET /app/health`
- **Description**: Retrieve static health resources page for new migrants, offering general health-related information. This page also includes a button to search for health services and a button to return to the home page.
- **Responses**:
  - `200 OK`: Health resources retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "content": "Welcome to the Health Resources page. Here, you'll find information on healthcare facilities, free clinics, and resources available to new members of the Chicago community.",
    "buttons": [
      {
        "name": "Search Health Services",
        "link": "/app/health-search"
      },
      {
        "name": "Home",
        "link": "/home"
      }
    ]
  }
  ```

## Search Health Services
### Retrieve Health Services
- **Endpoint**: `GET /app/health-search`
- **Description**: Retrieve a filterable table for searching health services based on query parameters like services, neighborhood, organization, or operating hours. This page includes a button to return to the home page.
- **Query Parameters**:
  - `services`: Filter by specific services (e.g., "medical", "dental").
  - `neighborhood`: Filter by location or neighborhood.
  - `organization`: Filter by health organizations or provider names.
  - `hours`: Filter by operating hours (e.g., "9am - 5pm").
- **Responses**:
  - `200 OK`: Health services retrieved successfully.
  - `400 Bad Request`: Invalid query parameters.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Request**:
  ```json
  {
    "services": "dental",
    "neighborhood": "South Side",
    "organization": "Health Center B",
    "hours": "10am - 6pm"
  }
  ```

## Health Page Buttons and Links
The health resources page has buttons to navigate to the health services search and to return to the home page.

- **Search Health Services**: This button leads to a filterable table of health services based on various criteria.
  - **Link**: `/app/health-search`
  - **Endpoint**: `GET /app/health-search`
  - **Description**: Navigate to the filterable table to find specific health services.

- **Return to Home Page**: This button returns to the home page.
  - **Link**: `/home`
  - **Endpoint**: `GET /app/home`
  - **Description**: Go back to the home page from the health resources page.

