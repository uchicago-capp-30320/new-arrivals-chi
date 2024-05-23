**NOTE:**
All user input that is manually entered will be sanitized before being added to tables.


### Association Tables for Many-to-Many Relationships

Since there are several 'many-to-many' relationships in the database, we will use association tables to represent these relationships. Below are the association tables that will be used in the database:

**languages\_organizations**:
`language_id` (int) – Foreign key referencing the _id_ column in the _language_ table.
`organization_id` (int) – Foreign key referencing the _id_ column in the _organization_ table.

**organizations\_hours**:
`organization_id` (int) – Foreign key referencing the _id_ column in the _organization_ table.
`hours_id` (int) – Foreign key referencing the _id_ column in the _hours_ table.

**organizations\_services**:
`organization_id` (int) – Foreign key referencing the _id_ column in the _organization_ table.
`service_id` (int) – Foreign key referencing the _id_ column in the _service_ table.


### Main Tables

<br/><br/>

**user**:

`id` (int) – Primary key for the user table. Will uniquely identify each user.
`email` (string) – Email associated with the user's account.
`password` (string) – Password associated with the user's account. Hashed for security.
`organization_id` (int) – Foreign key referencing the _id_ column in _organization_ table.


<br/><br/>

**organization**:

`id` (int) – Primary key for the organization table. Will uniquely identify each organization.

`name` (string) – Name of organization.

`location_id` (int) – Foreign key referencing the _id_ column in _location_ table.

`hours_id` (int) – Foreign key referencing the _id_ column in _hours_ table.

`phone` (string) – Primary external contact number for the organization. This will include the country code which will be able to be selected by the user from dropdown (information from data file)

`image_path` (string) – Path to corresponding organization logo; stored in cloud.

`status` (string) – Indicates the organization's status eg: ACTIVE, HIDDEN, SUSPENDED.


<br/><br/>


**language**:

`id` (int) – Primary key for the language table.

`language` (string) – A single language spoken at the organization.


<br/><br/>


**hours**:

`id` (int) – Primary key for the hours table.

`day_of_week` (int) – Day of the week when the organization operates. Will use ISO week-numbering: 1 = Monday … 7 = Sunday.

`opening_time` (time object) – Indicates time when the organization opens on the specified day.

`closing_time` (time object) – Indicates time when the organization opens on the specified day.


NOTE: Structure of this table allows for organizations to include breaks within their days. example: 

<table><tbody><tr><td><i>org_id</i></td><td><i>day_of_week</i></td><td><i>opening_time</i></td><td><i>closing_time</i></td></tr><tr><td>1</td><td>1</td><td>9:00 AM</td><td>11:00 AM</td></tr><tr><td>1</td><td>1</td><td>2:00 PM</td><td>7:00 PM</td></tr></tbody></table>

<br/><br/>


**services**:

`id` (int) – Primary key for the service table.

`category` (string) – Overarching category type of the service. Ex: Health, Legal etc.  Will have table of enumerated options saved in a backend layer to help with translation.

`service` (string) – Type of service. Will have table of enumerated options saved in a backend layer to help with translation.

`access` (string) - Mode of access for the service provided by the organization. Walk-Ins Only, Appointments Only, etc.

`service_note` (string) – More specified notes about the service. Provides the ability for organizations to give more information about the service they provide.


<br/><br/>


**service\_date**:

`id` (int) -  Primary key for the service date table.

`service_id` (int) – Foreign key referencing the _id_ column in the _service_ table.

`date` (date object) – Start date of the service.

`start_time` (time object) – Indicates time when the service starts on the specified day.

`end_time` (time object) – Indicates time when the service ends on the specified day.

`repeat` (Enum) - Specifies the frequency of the recurring service. 1 = Every day, 2 = Every week, 3 = Every month, 4 = Every other week.


<br/><br/>



**location**:

`id` (int) -  Primary key for the location table.

`street_address` (string) – Physical street address of the organization.

`zip_code` (string) – Zip code of the organization. Plan to use association tables to match zip codes to nearby Chicago neighborhoods.

`city` (string) – City that the organization is located within.

`state` (string) – State that the organization is located within.

`primary_location` (int) – Flag to indicate if this location is the primary location of associated organization.

`neighboorhood` (string) – Neighborhood in which the organization is located within. 
