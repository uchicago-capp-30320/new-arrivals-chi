# New Arrivals Chi - Architecture

## Architecture Overview

New Arrivals Chi is a web-based application that relies on a client server architecture to support its functionality. Divided into two main components the client (the frontend) and the server (the backend).

The client represents the user-facing part of the application. It interacts with the user, accepts input, and displays output. The client sends requests to the server and displays the responses received from the server. While the client is developed for browser access from various devices, user and stakeholder interviews highlighted the importance for the website to be easily accessible on mobile devices.

The server is responsible for processing client requests, application logic, and managing database resources. The server primarily manages user authentication, processes data, retrieves and responds to user requests. The server is the sole component of the application authorized to interface our PostgreSQL relational database.

Communication between the client and the server is completed with HTTP protocols. When a user interacts with New Arrivals Chi through their web browser, the browser sends an HTTP request to the New Arrivals Chi  server, which then processes these requests and sends back the appropriate responses, which are then displayed in the user's browser.

Our application relies on a monolithic architecture, consisting of a single server that will host the platform. This allows for a more simple development and deployment process as our application exists in a single codebase. We believe this scheme will be sufficient for our needs, as we do not anticipate a high volume of requests.

## Key Details
**Client (Frontend)**:
-   **HTML**: Responsible for the structure and content of the website.
-   **CSS**: Used for styling HTML elements, defining layout, colors, fonts, etc.

**Server (Backend)**:
-  **Application & Web Server**:  Written in Python, Flask is used to define routes, receives and respond to HTTP requests, interact with the database, and render responses.
-  **Database**: We use a PostgreSQL relational database to securely store user authentication data, as well as information about organizations and services. The relational models are further explained in `models/models.md`.
- **Cloud Storage**: We utilize an AWS S3 bucket as our cloud storage provider. The primary purpose of this bucket is to house the logo images for each organization within our system.

**Communication between Frontend and Backend**:
-   **HTTP/HTTPS Protocol**: The communication between the client and server happens over HTTP protocol (with the plan shift to a HTTPS when we deploy our web server). We use HTTP methods like GET, POST, DELETE to send requests to the server.

**Security**:
  -   **Authentication and Authorization**: We implement user authentication and authorization with Flask-Login, which allows us to verify user credentials, set session variables, and protect routes. Passwords and vulnerable information is hashed with bcrypt before storing them in the database. This ensures that even if the database is compromised, the passwords remain secure. Additionally, we enforce proper authorization checks within our routes to ensure that users only have access to the resources they are permitted to interact with. Notably, standard website visitors are not required to have authentication to access the platform. Authorization is solely required for website administrators and representatives from the Chicago community organization; these users are subjected to distinct levels of authentication.
  -   **Input Validation and Sanitization**: Our data is ingested from our authorized user client; nonetheless, we employ various techniques to ensure the protection of our systems and cleanliness of our database. Input is validated within our codebase to ensure that the data submitted by users meets our defined criteria before it is processed by the application. Moreover, our data is also sanitized to prevent common security vulnerabilities. We prevent SQL injection attacks by using parameterized queries and cross-site scripting attacks by properly escaping and removing code that could be used to execute scripts.

## Data Ingestion
The current version of New Arrivals Chi does not utilize any data pipelines or APIs to populate our databases (at the time of creation such data sources containing comprehensive, updated information for new arrivals does not exist for Chicago). The New Arrivals Chi platform instead relies on input data from our authenticated users. This data is detailed information about the organizations, the services provided, and additional necessary information for newly arrived individuals to access such resources. Given that our data relies on user input, we employ a rigorous validation and sanitization process before it is added to our application – this process is detailed above in the _Input Validation and Sanitization_ section.

## Data Flow
The ingested data will be stored in our own database. The information flows from the web app (when users insert or add data regarding their organization) and to the web app (meaning that the database’s information will populate the web application).

## Module Relationships

The following diagram shows how our application's modules are related with each other. We have a 'log in' module, which, along with a 'sign up' module, interact with the database to either upload or read a user's data.

As the diagram shows, all of the other services in the application (food, legal information, etc.) are managed by a Flask layer that interacts with the database. Moreover, the Flask layer will be in charge with reading the database to populate the user interface, an it will also handle any data uploads to the database.

![SWE-Diagram (2)](https://github.com/uchicago-capp-30320/new-arrivals-chi/assets/67844597/329f4fd9-a5a0-463f-a108-2005a3800470)


## User’s Application Architecture Overview
The primary focus of this application is to simplify and streamline access to essential resources for newly arrived individuals, as well as provide organizations with a platform to maintain up-to-date information about supplies and services. As such, it would be counterintuitive to our mission to expect users of New Arrivals Chi to understand the complexities of the application’s architecture. A user should be able to utilize and navigate New Arrivals Chi just like any other general website. The only aspect of the architecture that users should be aware of is our security and data collection standards. For general website visitors, they should understand that their data will not be stored anywhere. For authenticated users (administrators and organizations), it will be important to highlight the security of our database, especially regarding password storage.
