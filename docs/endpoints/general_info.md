# General Information Endpoint Documentation

The general information page provides users with static content about Chicago and the various resources available to new migrants.

The documentation is divided into the following sections:
- [Retrieve General Information Content](#retrieve-general-information-content)
- [General Information Page Buttons and Links](#general-information-page-buttons-and-links)


## Retrieve General Information Content
### Get General Information Content
- **Endpoint**: `GET /general_information`
- **Description**: Retrieve static content for the general information page, providing information about Chicago and resources for new migrants.
- **Responses**:
  - `200 OK`: General information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
- **Example Response**:
  ```json
  {
    "content": "Welcome to Chicago! Here are some resources to help you get started, including public transportation, educational facilities, and city services...",
    "buttons": [
      {
        "name": "Home Page",
        "link": "/"
      }
    ]
  }
  ```

## General Information Page Buttons and Links
This section describes the buttons and links on the general information page, providing navigation options for users.

### Return to Home Page
- **Endpoint**: ``GET /`
- **Description**:   Button to navigate back to the home page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
