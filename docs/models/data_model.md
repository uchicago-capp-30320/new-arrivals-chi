**NOTE:**
All user input that is manually entered will be sanitized before being added to tables.

<br/><br/> 

**organization\_table**:

`org_id` (int)_–_ Primary key for the organization table. Will uniquely identify each organization.

`organization_name` (string) – Name of organization.

`email` (string) – Email associated with the organization's account.

`password` (string) – Password associated with the organization's account. Hashed for security.

`street_address` (string) – Physical street address of the organization.

`zip_code` (string) – Zip code of the organization. Plan to use association tables to match zip codes to nearby Chicago neighborhoods.

`city` (string) – City that the organization is located within.

`state` (string) – State that the organization is located within.

`phone` (string) – Primary external contact number for the organization. This will include the country code which will be able to be selected by the user from dropdown (information from data file)

`image_path` (string) – Path to corresponding organization logo; stored in cloud.

`active` (Datetime) – Indicates the organization's admin active status. Not null indicates active and time when it was activated, null indicates suspended.

`deleted` (Datetime) – Indicates whether the organization's deleted status. Not null indicates indicates time this organization was deleted, null indicates active. Allows for soft delete.

`visible` (Datetime) – Indicates the organization is visible on the portal to users. Not null indicates visible and time when it was activated, null indicates invisible.


<br/><br/> 


**language\_table**:

`lang_id` (int)_–_ Primary key for the language table.

`org_id` (int) – Foreign key referencing the _org\_id_ column in _organization\_table_.

`language` (string) – A single language spoken at the organization.  


<br/><br/> 

  
**hours\_table**:

`hours_id` (int)_–_ Primary key for the hours table.

`org_id` (int) – Foreign key referencing the _org\_id_ column in  _organization\_table_.

`day_of_week` (int) – Day of the week when the organization operates. Will use ISO week-numbering: 1 = Monday … 7 = Sunday.

`opening_time` (time object) – Indicates time when the organization opens on the specified day.

`closing_time` (time object) – Indicates time when the organization opens on the specified day.


NOTE: Structure of this table allows for organizations to include breaks within their days. example: 

<table><tbody><tr><td><i>org_id</i></td><td><i>day_of_week</i></td><td><i>opening_time</i></td><td><i>closing_time</i></td></tr><tr><td>1</td><td>1</td><td>9:00 AM</td><td>11:00 AM</td></tr><tr><td>1</td><td>1</td><td>2:00 PM</td><td>7:00 PM</td></tr></tbody></table>

<br/><br/> 


**hours\_exception\_table**:

`hours_exception_id` (int)_–_ Primary key for the hours table.

`org_id` (int) – Foreign key referencing the _org\_id_ column in _organization_table_.

`exception_start` (date object) – Indicates the date in which the modfied hours start.

`exception_end` (date object) – Indicates the date in which the modfied hours end.

`opening_time` (time object) – Indicates time when the organization opens on the specified day.

`closing_time` (time object) – Indicates time when the organization opens on the specified day.


<br/><br/> 

  
**supply\_table**:

`supply_id` (int)_–_ Primary key for the supply table.

`org_id` (int) – Foreign key referencing the _org\_id_ column in _organization\_table_.

`category` (string) – Overarching category type of the supply item. Ex: Clothing, Home, Health, etc. Will have table of enumerated options saved in a backend layer to help with translation.

`item_type` (string) – Type of item. Ex: Jackets, Pants, etc. Will have table of enumerated options saved in a backend layer to help with translation.

`item_status` (int) – Indicates whether the item is available at the organization. 1 indicates available, 0 indicates unavailable.

`logo_path` (string) – Path to corresponding item logo; stored in cloud.

`item_note` (string) – More specified notes about the items. Provides the ability for organizations to give more information about the items in stock that they have.


<br/><br/> 


**services\_table**:

`services_id` (int) – Primary key for the service table.

`org_id` (int) – Foreign key referencing the _org_id_ column in the organization\_table.

`category` (string) – Overarching category type of the service. Ex: Health, Legal etc.  Will have table of enumerated options saved in a backend layer to help with translation.

`service` (string) – Type of service. Will have table of enumerated options saved in a backend layer to help with translation.

`service_description` (string) – Explanation of the service.

`access` (string) - Mode of access for the service provided by the organization. Walk-Ins Only, Appointments Only, etc.

`service_note` (string) – More specified notes about the service. Provides the ability for organizations to give more information about the service they provide.  

`alt_location` (string) – Street address of the alternate location for the service. Not null indicates alternate location, null indicates normal organization location.

`alt_zip_code` (string) – Zip code of the alternate location. Plan to use association tables to match zip codes to nearby Chicago neighborhoods.

`alt_city` (string) – City that the alternate location is located within.

`alt_state` (string) – State that the alternate location is located within.


<br/><br/> 


**service\_date\_table**:

`service_date_id` (int) -  Primary key for the service date table.

`org_id` (int) – Foreign key referencing the org\_id column in the organization\_table.

`service_id` (int) – Foreign key referencing the service\_id column in the service\_table.

`start_date` (date object) – Start date of the service.

`day_of_week` (int) – Day of the week when the organization operates.  Will use ISO week-numbering: 1 = Monday … 7 = Sunday.

`opening_time` (time object) – Indicates time when the organization opens on the specified day.

`closing_time` (time object) – Indicates time when the organization opens on the specified day.

`frequency` (String) - Specifies the frequency of the recurring service.