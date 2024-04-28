# Legal Flow Endpoint Documentation

The legal flow guides users through a series of questions to determine the appropriate legal resources based on their individual circumstances. It provides an organized pathway for users seeking various forms of legal support, such as Temporary Protected Status (TPS), work authorization, asylum, and humanitarian parole.

The documentation is divided into the following sections:
- [Determine Legal Flow](#determine-legal-flow)
- [Legal Flow Outcomes](#legal-flow-outcomes)
- [Legal Page Buttons and Links](#legal-page-buttons-and-links)

## Determine Legal Flow
### Get Legal Flow Content
- **Endpoint**: `GET /legal`
- **Description**: Retrieve the legal flowchart, guiding users through a series of questions to identify the appropriate legal resource.
- **Responses**:
  - `200 OK`: Legal flowchart content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

## Legal Flow Outcomes
### Temporary Protected Status (TPS) - Basic
- **Endpoint**: `GET /legal/temporary-protected-status-basic`
- **Description**: Provides basic information on the rights a privileges of those Temporary Protected Status for those who have applied or already been approved for TPS.
- **Responses**:
  - `200 OK`: TPS information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.


### Temporary Protected Status (TPS) - Guide
- **Endpoint**: `GET /legal/temporary-protected-status-guide`
- **Description**: Provides guide for those applying for TPS as well as information about workshops. This page also includes the general information from the basic page.
- **Responses**:
  - `200 OK`: TPS information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Work Authorization - Basic
- **Endpoint**: `GET /legal/work-authorization-basic`
- **Description**: Provides basic information on the rights a privileges of work authorization for those who have applied or already been approved for work authorization.
- **Responses**:
  - `200 OK`: Work authorization information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

  ### Work Authorization - Guide
- **Endpoint**: `GET /legal/work-authorization-guide`
- **Description**: Provides guide for those applying for work authorization. This page also includes the general information from the basic page.
- **Responses**:
  - `200 OK`: Work authorization information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Asylum - Basic
- **Endpoint**: `GET /legal/asylum-basic`
- **Description**: Provides basic information on the rights a privileges of asylum status for those who have applied or already been approved for asylum status.
- **Responses**:
  - `200 OK`: Asylum information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Asylum - Guide
- **Endpoint**: `GET /legal/asylum-guide`
- **Description**: Provides guide for those applying for asylum status. This page also includes the general information from the basic page.
- **Responses**:
  - `200 OK`: Asylum information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Humanitarian Parole - Basic
- **Endpoint**: `GET /legal/humanitarian-parole-basic`
- **Description**: Provides basic information on the rights a privileges of humanitarian parole for those who have applied or already been approved for humanitarian parole.
- **Responses**:
  - `200 OK`: Humanitarian parole information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Humanitarian Parole - Guide
- **Endpoint**: `GET /legal/humanitarian-parole-guide`
- **Description**: Provides guide for those applying for humanitarian parole. This page also includes the general information from the basic page.
  - `200 OK`: Humanitarian parole information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Rights as a Worker
- **Endpoint**: `GET /legal/worker-rights`
- **Description**: Static page with information about workers' rights.
- **Responses**:
  - `200 OK`: Workers rights information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Rights as a Renter
- **Endpoint**: `/legal/renter-rights`
- **Description**: Static page with information about renters' rights.
- **Responses**:
  - `200 OK`: Renters rights information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

## Legal Page Buttons and Links
This section describes the buttons and links on the legal flow page, guiding users to relevant information.

### General Legal Support
- **Endpoint**: `/legal/legal-support`
- **Description**:  Button linking to a static page with contact information for recommended lawyers/legal support. This button should be on every end page regardless of flow.
- **Responses**:
  - `200 OK`: Legal Support information retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.

### Return to Home Page
- **Endpoint**: ``GET /`
- **Description**:   Button to navigate back to the home page.
- **Responses**:
  - `200 OK`: Home page content retrieved successfully.
  - `500 Internal Server Error`: Indicates a server error.
