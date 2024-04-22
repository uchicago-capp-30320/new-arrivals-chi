# Admin Authentication Endpoints

This document describes the authentication and account management endpoints for administrators in New Arrivals Chi.

TODO:
- Define all admin endpoints
- Confirm methods
- Confirm update parameters
- Define desired response

## /admin/login
- **Description**: Endpoint for Admin login.
- **Method**: POST
- **Parameters**:
  - `email`: Admin's email address.
  - `password`: Admin's password.
- **Response**: TODO

## /admin/create_org
- **Description**: Endpoint for the admin to add and organization to the database
- **Method**: PUT
- **Parameters**: JSON object with fields (e.g., `address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Response**: 

## /admin/update_org_status
- **Description**: Endpoint for the admin to edit, suspect, or delete and organizations profile
- **Method**: 
- **Parameters**: 
- **Response**: 

## /admin/org_update
- **Description**: Endpoint for  editing organization information on behalf of an organization (e.g., address, phone, hours, services, languages, supplies and services).
- **Method**: PUT
- **Parameters**: JSON object with updated fields (e.g., `address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Response**: TODO
- **Similarity with /org/update**: While both `//admin/org_update` and `/org/update` can perform updates on organization profiles, they serve different user roles:
    - **/admin/org_update** is intended for administrators to change the organization's status or perform administrative actions.
    - **/org/update** is for organization users to update their own information.





