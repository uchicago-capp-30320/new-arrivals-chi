# General Information Endpoint Documentation

The general information page provides users with static content about Chicago and the various resources available to new migrants. 

## Retrieve General Information Content
### Get General Information Content
- **Endpoint**: `GET /app/information/general`
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
        "link": "/home"
      }
    ]
  }
  ```

## General Information Page Buttons and Links
This section describes the buttons and links on the general information page, providing navigation options for users.

- **Home Page**: This button allows users to return to the home page.
  - **Link**: `/home`
  - **Endpoint**: `GET /app/home`
  - **Description**: Returns to the home page from the general information page.

