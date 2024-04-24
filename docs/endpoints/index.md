
# Summary of Endpoints for New Arrivals Chi

## [Home Page](home.md)
- [**Get Home Page Content**:](home.md#get-home-page-content) `GET /app/home` — Retrieve content for the home page, including sections and action buttons.

## [General Information Page](general_info.md)
- [**Get General Information Content**:](general_info.md#get-general-information-content) `GET /app/information/general` — Retrieve general information content about Chicago and resources for new migrants.

## [Health Resources Page](health.md)
- [**Get Health Resources Content**:](health.md#get-health-resources-page-content) `GET /app/health` — Retrieve the static health resources page.
- [**Retrieve Health Services**:](health.md#search-health-services) `GET /app/health-search` — Retrieve health services based on query parameters like services, neighborhood, organization, or operating hours.

## [Admin Page](admin.md)
### [Admin Login](admin.md#admin-login)
- [**Authenticate Admin**:](admin.md#authenticate-admin) `POST /app/auth/admin-login` — Log in to the admin page with admin credentials.

### [Admin Dashboard](admin.md#get-admin-page-content)
- [**Get Admin Dashboard Content**:](admin.md#get-admin-page-content) `GET /app/admin/dashboard` — Retrieve the admin dashboard content, including an overview of organizations and admin-related tasks.

### [Admin Tasks](admin.md#admin-page-buttons-and-links)
- **Add Organization**: `POST /app/admin/organization` — Add a new organization with required information.
- **Edit Organization**: `PUT /app/admin/organization` — Edit an existing organization's profile details.
- **Delete Organization**: `DELETE /app/admin/organization/{username}` — Delete an organization by its username.
- **Logout**: `POST /app/auth/admin-logout` — Log out of the admin session.

## [Organization Page](organization.md#admin.md)
### [Organization Login](organization.md#organization-login.md)
- [**Authenticate Organization**:](organization.md#authenticate-organization) `POST /app/auth/organization-login` — Log in to the organization page with credentials.

### Organization Profile
- [**Get Organization Profile**:](anization.md#get-organization-profile)`GET /app/organization/profile` — Retrieve the profile information of the logged-in organization.
- [**Update Organization Profile**:](anization.md#update-organization-profile) `PUT /app/organization/profile` — Update the organization's profile information.
- [**Delete Organization Account**](anization.md#Delete Organization Account) `DELETE /app/organization/profile` — Delete the logged-in organization's account.
home page from the organization page.
- **Logout**: `POST /app/auth/org-logout` — Log out and end the organization's session.


### Organization Setup
- [**Create Organization Account**:](organization.md#create-organization-account) `POST /app/organization/setup` — Set up a new organization account via a direct link.

## Bug Reporting
- **Report a Bug**: `POST /app/bugs/report` — Submit a bug report with a description of the issue.

## Toggle Language
- **Toggle Language**: `POST /app/settings/language` — Toggle the website's language between English and Spanish.
