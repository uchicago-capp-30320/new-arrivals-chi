**organization\_table**:

_org\_id_ (UUID)_–_ Primary key for the organization table. Uniquely identifies each organization. (NOTE TO TEAM: Does UUID seem right?).

_organization\_name_ (string) – Name of organization.

_email_ (string) – Email associated with the organization's account.

_password_ (string) – Password associated with the organization's account. Hashed for security.

_address_ (string) – Physical address of the organization.

_neighborhood_ (string) – Neighborhood where the organization is located. (NOTE: considering calculating neighborhoods from address)

_phone_ (string) – Primary external contact number for the organization.

_image\_path_ (String) – Path to corresponding organization logo; stored in cloud.

_status_ (int) – Flag to indicate whether the organization's admin status. 1 indicates active, 0 indicates suspended, -1 indicates deleted. (NOTE TO TEAM: do we need deleted?)

_visibility_ (int) – Flag to indicate whether the organization is visible on the portal to users. 1 indicates visible to the users, 0 indicates hidden.


  

**language\_table**:

_org\_id_ (UUID) – Foreign key referencing the org\_id column in the organization\_table.

_language_ (string) – A single language spoken at the organization.

  

**hours\_table**:

_org\_id_ (UUID) – Foreign key referencing the org\_id column in the organization\_table.

_service\_id_ (UUID) – Foreign key referencing the service\_id column in the service\_table.

_day\_of\_week_ (int) – Day of the week when the organization operates. 1 = Monday … 7 = Sunday.

_opening\_time_ (time object) – Indicates time when the organization opens on the specified day.

_closing\_time_ (time object) – Indicates time when the organization opens on the specified day.

_date_ (date object)

NOTE: Structure of this table allows for organizations to include breaks within their days. example: 

<table><tbody><tr><td><i>org_id</i></td><td><i>day_of_week</i></td><td><i>opening_time</i></td><td><i>closing_time</i></td></tr><tr><td>1</td><td>1</td><td>9:00 AM</td><td>11:00 AM</td></tr><tr><td>1</td><td>1</td><td>2:00 PM</td><td>7:00 PM</td></tr></tbody></table>

NOTE TO TEAM: Would there be any use in a primary key here?

  

**supply\_table**:

_org\_id_ (UUID) – Foreign key referencing the org\_id column in the organization\_table.

_category_ (string) – Overarching category type of the supply item. Ex: Clothing, Home, Health, etc.

_item\_type_ (string) – Type of item. Ex: Jackets, Pants, etc.

_item\_status_ (int/string?) – Indicates whether the item is available at the organization. 1 indicates available, 0 indicates available. (NOTE TO TEAM: low stock?)

_logo\_path_ (string) – Path to corresponding item logo; stored in cloud.

_item\_note_ (string) – More specified notes about the items. Provides the ability for organizations to give more information about the items in stock that they have.



  
**services\_table**:

_service\_id_ (UUID)_–_ Primary key for the service table. Uniquely identifies each service. 

_org\_id_ (UUID) – Foreign key referencing the org\_id column in the organization\_table.

_category_ (string) – Overarching category type of the service. Ex: Health, Legal etc.

_service_ (string) – Type of service.

_service\_description_ (string) – Explanation of the service.

_alt\_location\_flag_ (int) – Indicates whether there is an alternate location for the service. 1 indicates alternate location, 0 indicates normal organization location.

_alt\_location_ (string) – Address of the alternate location

_access_ (string) - Mode of access for the service provided by the organization. Walk-Ins Only, Appointments Only, etc.

_service\_note_ (string) – More specified notes about the service. Provides the ability for organizations to give more information about the service they provide.


  
**service\_date\_table**:

_org\_id_ (UUID) – Foreign key referencing the org\_id column in the organization\_table.

_service\_id_ (UUID) – Foreign key referencing the service\_id column in the service\_table.

_start\_date_ (date object) – Start date of the service.

_day\_of\_week_ (int) – Day of the week when the organization operates. 1 = Monday … 7 = Sunday.

_opening\_time_ (time object) – Indicates time when the organization opens on the specified day.

_closing\_time_ (time object) – Indicates time when the organization opens on the specified day.

_recurring_ (int) – Flag that indicates whether the services recurring. 1  indicates recurring, 0 indicates not recurring.

_frequency_ (String) - Specifies the frequency of the recurring service.
