# New Arrivals Chi - Model

## Association Tables
Tables for Many-to-Many relationships

**languages_organizations**

| Name           | Type    | Description                                     |
|----------------|---------|-------------------------------------------------|
| language_id    | int     | Foreign key referencing the id column in languages table. Primary key. |
| organization_id| int     | Foreign key referencing the id column in organizations table. Primary key. |  

<br>

**organizations_hours**
| Name           | Type    | Description                                     |
|----------------|---------|-------------------------------------------------|
| hours_id       | int     | Foreign key referencing the id column in hours table. Primary key. |
| organization_id| int     | Foreign key referencing the id column in organizations table. Primary key. |

<br/>

**organizations_services**
| Name           | Type    | Description                                     |
|----------------|---------|-------------------------------------------------|
| service_id     | int     | Foreign key referencing the id column in services table. Primary key. |
| organization_id| int     | Foreign key referencing the id column in organizations table. Primary key. |

<br/><br/>

## Data Tables
**user**
| Name             | Type      | Description                                       |
|------------------|-----------|---------------------------------------------------|
| id               | int       | Primary key for the users table.                  |
| email            | string    | Email of the user.                                |
| password         | string    | Password of the user.                             |
| organization_id  | ForeignKey(Organization)       | Foreign key referencing the id column in organizations table. |
| role             | Enum      | Role of the user within the organization. Example: administrator, standard, moderator, etc. |
| created_at       | timestamp | UTC timestamp indicating when the user was created. |
| deleted_at       | timestamp | UTC timestamp indicating when the user was soft deleted. |
| approved_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who approved this user. |

Relationships:
- organization: Represents the relationship between the user and organization. Each user belongs to an organization.

<br>

**organization**
| Name        | Type    | Description                                                 |
|-------------|---------|-------------------------------------------------------------|
| id          | int     | Primary key for the organization table.                     |
| name        | string  | Name of organization.                                       |
| location_id | ForeignKey(Location)     | Foreign key referencing the id column in location table.    |
| hours_id    | ForeignKey(Hours)     | Foreign key referencing the id column in hours table.       |
| phone       | string  | Primary external contact number for the organization.       |
| image_path  | string  | Path to corresponding organization logo; stored in cloud.   |
| status      | string  | Indicates the organization's status eg: ACTIVE, HIDDEN, SUSPENDED. |
| created_at       | timestamp | UTC timestamp indicating when the organization was created. |
| deleted_at       | timestamp | UTC timestamp indicating when the organization was soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created this user. |

 Relationships:
 - users: Represents the relationship between the organization and users. Each organization can have multiple users associated with it. 
 - languages: Represents the relationship between the organization and languages. Each organization can support multiple languages. 
 - services: Represents the relationship between the organization and services. Each organization can provide multiple services. 
 - hours: Represents the relationship between the organization and hours. Each organization can have multiple operating hours.

<br>

**language**
| Name        | Type    | Description |
|-------------|---------|-------------|
| id          | int     | Primary key for the language table. |
| language    | string  | A single language spoken at the organization. |
| created_at       | timestamp | UTC timestamp indicating when the language was created. |
| deleted_at       | timestamp | UTC timestamp indicating when the language was soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created this language. |

Relationships:
- organizations: Represents the relationship between the language and organizations. Each language can be supported by multiple organizations.`
  
<br>

**hours**
| Name          | Type      | Description |
|---------------|-----------|-------------|
| id            | int       | Primary key for the hours table. |
| day_of_week   | int       | Day of the week when the organization operates. Will use ISO week-numbering: 1 = Monday … 7 = Sunday. |
| opening_time  | time      | Indicates time when the organization opens on the specified day. |
| closing_time  | time      | Indicates time when the organization opens on the specified day. |
| created_at       | timestamp | UTC timestamp indicating when the hours were created. |
| deleted_at       | timestamp | UTC timestamp indicating when the hours were soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created these hours. |

 Relationships:
- organizations: Represents the relationship between the hours and organizations. Each set of hours can be associated with multiple organizations.

<br>

**service**
| Name          | Type      | Description |
|---------------|-----------|-------------|
| id            | int       | Primary key for the service table. |
| category      | string    | Overarching category type of the service. Ex: Health, Legal etc. |
| service       | string    | Type of service. |
| access        | string    | Mode of access for the service provided by the organization. |
| service_note  | string    | More specified notes about the service. |
| created_at       | timestamp | UTC timestamp indicating when the service was created. |
| deleted_at       | timestamp | UTC timestamp indicating when the service was soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created this service. |

Relationships:
- organizations: Represents the relationship between the services and organizations. Each service can be provided by multiple organizations.
- service_dates: Represents the relationship between the services and service dates. Each service can have multiple service dates associated with it.
- locations: Represents the relationship between the services and locations. Each service can be offered at multiple locations.

<br>

**service_dates**
| Name          | Type      | Description |
|---------------|-----------|-------------|
| id            | int       | Primary key for the service date table. |
| date          | date      | Start date of the service. |
| start_time    | time      | Indicates time when the service starts on the specified day. |
| end_time      | time      | Indicates time when the service ends on the specified day. |
| repeat        | Enum      | Specifies the frequency of the recurring service. 1 = Every day, 2 = Every week, 3 = Every month, 4 = Every other week. |
| org_id          | ForeignKey(Organization)      | Foreign key referencing the id column in the organization table. |
| service_id    | ForeignKey(Service)        | Foreign key referencing the id column in service table. |
| created_at       | timestamp | UTC timestamp indicating when the service hours were created. |
| deleted_at       | timestamp | UTC timestamp indicating when the service hours were soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created these service hours. |

Relationships:
- service: Represents the relationship between the service dates and services. Each service date is associated with a specific service.

<br>

**locations**
| Name            | Type    | Description |
|-----------------|---------|-------------|
| id              | int     | Primary key for the location table. |
| org_id          | ForeignKey(Organization)      | Foreign key referencing the id column in the organization table. |
| street_address  | string  | Physical street address of the organization. |
| zip_code        | string  | Zip code of the organization. Plan to use association tables to match zip codes to nearby Chicago neighborhoods. |
| city            | string  | City that the organization is located within. |
| state           | string  | State that the organization is located within. |
| primary_location| int     | Flag to indicate if this location is the primary location of associated organization. |
| created_at       | timestamp | UTC timestamp indicating when the service hours were created. |
| deleted_at       | timestamp | UTC timestamp indicating when the service hours were soft deleted. |
| created_by      | ForeignKey(User)       | Foreign key referencing the id column in users table, indicating the user who created these service hours. |
