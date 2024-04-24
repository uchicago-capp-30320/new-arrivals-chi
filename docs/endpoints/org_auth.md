# Organization Authentication Endpoints

This document describes the authentication and account management endpoints for organizations in New Arrivals Chi.

TODO:
- Define all organization endpoints
- Confirm methods
- Confirm update parameters
- Define desired response

## /org/login
- **Description**: Endpoint for organization login.
- **Method**: POST
- **Parameters**:
  - `email`: Organization's email address.
  - `password`: Organization's password.
- **Response**: TODO

## /org/update
- **Description**: Endpoint for updating organization information (e.g., address, phone, hours, services, languages, supplies and services).
- **Method**: PUT
- **Parameters**: JSON object with updated fields (e.g., `address`, `phone`, `hours`, `languages`, `supplies`, `services`).
- **Response**: TODO
- **Similarity with /admin/org_update**: While both `//admin/org_update` and `/org/update` can perform updates on organization profiles, they serve different user roles:
    - **/admin/org_update** is intended for administrators to change the organization's status or perform administrative actions.
    - **/org/update** is for organization users to update their own information.

## /org/change-password
- **Description**: Endpoint to change the organization's password.
- **Method**: PUT
- **Parameters**:
  - `old_password`: Current password.
  - `new_password`: New password.
- **Response**: TODO

## /org/deactivate
- **Description**: Endpoint to deactivate an organization's account.
- **Method**: POST
- **Parameters**: None.
- **Response**: TODO
