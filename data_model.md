**NOTE:**
All user input that is manually entered will be sanitized before being added to tables.

**organization\_table**:

_org\_id_ (int)_–_ Primary key for the organization table. Will uniquely identifies each organization.

_organization\_name_ (string) – Name of organization.

_email_ (string) – Email associated with the organization's account.

_password_ (string) – Password associated with the organization's account. Hashed for security.

_street\_address_ (string) – Physical street address of the organization.

_zip\_code_ (string) – Zip code of the organization. Plan to use association tables to match zip codes to nearby Chicago neighborhoods.

_city_ (string) – City that the organization is located within.

_state_ (string) – State that the organization is located within.

_phone_ (string) – Primary external contact number for the organization. This will include the country code which will be able to be selected by the user from dropdown (information from data file)

_image\_path_ (string) – Path to corresponding organization logo; stored in cloud.

_active_ (Datetime) – Indicates whether the organization's admin active status. Not null indicates active and time when it was activated, null indicates suspended.

_deleted_ (Datetime) – Indicates whether the organization's deleted status. Not null indicates indicates time this organization was deleted, null indicates active. Allows for soft delete.

_visible_ (Datetime) – Indicates whether the organization is visible on the portal to users. Not null indicates visible and time when it was activated, null indicates invisible.


<br/><br/> 


**language\_table**:

_lang\_id_ (int)_–_ Primary key for the language table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_language_ (string) – A single language spoken at the organization.  


<br/><br/> 

  
**hours\_table**:

_hours\_id_ (int)_–_ Primary key for the hours table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_day\_of\_week_ (int) – Day of the week when the organization operates. Will use ISO week-numbering: 1 = Monday … 7 = Sunday.

_opening\_time_ (time object) – Indicates time when the organization opens on the specified day.

_closing\_time_ (time object) – Indicates time when the organization opens on the specified day.


NOTE: Structure of this table allows for organizations to include breaks within their days. example: 

<table><tbody><tr><td><i>org_id</i></td><td><i>day_of_week</i></td><td><i>opening_time</i></td><td><i>closing_time</i></td></tr><tr><td>1</td><td>1</td><td>9:00 AM</td><td>11:00 AM</td></tr><tr><td>1</td><td>1</td><td>2:00 PM</td><td>7:00 PM</td></tr></tbody></table>

<br/><br/> 


**hours\_exception\_table**:

_hours\_exception\_id_ (int)_–_ Primary key for the hours table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_exception\_start_ (date object) – Indicates the date in which the modfied hours start.

_exception\_end_ (date object) – Indicates the date in which the modfied hours end.

_opening\_time_ (time object) – Indicates time when the organization opens on the specified day.

_closing\_time_ (time object) – Indicates time when the organization opens on the specified day.


<br/><br/> 

  
**supply\_table**:

_supply\_id_ (int)_–_ Primary key for the supply table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_category_ (string) – Overarching category type of the supply item. Ex: Clothing, Home, Health, etc.

_item\_type_ (string) – Type of item. Ex: Jackets, Pants, etc.

_item\_status_ (int/string?) – Indicates whether the item is available at the organization. 1 indicates available, 0 indicates available. (NOTE TO TEAM: low stock?)

_logo\_path_ (string) – Path to corresponding item logo; stored in cloud

_item\_note_ (string) – More specified notes about the items. Provides the ability for organizations to give more information about the items in stock that they have.


<br/><br/> 


**services\_table**:

_service\_id_ (int)_–_ Primary key for the service table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_category_ (string) – Overarching category type of the service. Ex: Health, Legal etc.

_service_ (string) – Type of service.

_service\_description_ (string) – Explanation of the service.

_alt\_location\_flag_ (int) – Indicates whether there is an alternate location for the service. 1 indicates alternate location, 0 indicates normal organization location.

_alt\_location_ (string) – Address of the alternate location

_access_ (string) - Mode of access for the service provided by the organization. Walk-Ins Only, Appointments Only, etc.

_service\_note_ (string) – More specified notes about the service. Provides the ability for organizations to give more information about the service they provide.  


<br/><br/> 


**service\_date\_table**:

_service_date\_id_ (int)_–_ Primary key for the service date table.

_org\_id_ (int) – Foreign key referencing the org\_id column in the organization\_table.

_service\_id_ (int) – Foreign key referencing the service\_id column in the service\_table.

_start\_date_ (date object) – Start date of the service.

_day\_of\_week_ (int) – Day of the week when the organization operates. 1 = Monday … 7 = Sunday.

_opening\_time_ (time object) – Indicates time when the organization opens on the specified day.

_closing\_time_ (time object) – Indicates time when the organization opens on the specified day.

_frequency_ (String) - Specifies the frequency of the recurring service.
