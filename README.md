# New Arrivals Chi

New Arrivals Chi is a resource guide developed by six graduate students from the University of Chicago to help newly arrived individuals navigate the City of Chicago and its available resources. New Migrants often find themselves struggling with the complexities of accessing essential resources, from navigating systems to staying updated on what's available. Our goal is to provide accurate, up-to-date, and actionable information to address common challenges faced by newcomers.

The public facing site includes a guide for getting started in Chicago, legal support and health information. It also includes a two tiered login structure that allows organization to login and update their information, and site administrators to login and manage all organizations.

This project is student run in collaboration with various Community Based Organizations. It is a work in progress, and we look forward to expanding it to include additional services in the near future!

## Table of Contents

1.  [Running the Application](#running-the-application)
    1.  Project Structure
    2.  Installing
    3.  Running the Project
    4.  Running the Tests
    5.  Running the Data Migration
2.  [Using the Application](#using-the-application)
3.  [Design and Values](#design-and-values)
4.  [Next Steps](#next-steps)
5.  [Authors](#authors)
6.  [License](#license)
7.  [Acknowledgments](#acknowledgments)
8.  [Get in Touch](#get-in-touch)

# Running the Application

Follow these instructions to get the project running on your computer for development and testing.

### Project Structure 
*   `.github/`: This folder contains the templates and workflows for our github repository.
*   `docs/`: This folder contains documents outlining decisions made throughout the development process.
    * `decisions/`: This folder contains the decisions made regarding the various application components.
    * `design/`: This folder contains documentation for the design process.
    * `endpoints/`: This folder contains the enpoints for the pages of the application.
    * `models/`: This folder contains the data models for the database.
    * `style_templates/`: This folder contains the sylistic decisions to follow when contributing to the application.
*   `new_arrivals_chi/`: This folder contains the New Arrivals Chi application.
    * `app/`: This folder contains the frontend, backend, and database code for the application.
    * `migrations/`: This folder contains the migrations to establish the database.
*   `tests/`: This folder contains the test scripts for the application.

### Installing

Poetry:

1.  Install Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2.  Navigate to your the project directory and use Poetry to install project dependencies:
    ```bash
    poetry install
    ```


### Running the Project

1.  Navigate to your the project directory and use Poetry to update project dependencies:
    ```bash
    poetry update
    ```
    
3.  Activate the Poetry virutal environment:
    ```bash
    poetry shell
    ```

4.  Run application:
    ```bash
    python new_arrivals_chi/app/main.py
    ``` 

### Running the Tests

- Run all tests:
  ```bash
  poetry run pytest
  ```

- Run a specific test:
  ```bash
  poetry run pytest tests/app_home_test.py::test_home_page_status
  ```
  
- Run database tests:
  ```bash
  poetry run pytest tests/db_test.py
  ```

### Creating a database migration

1.  Activate the Poetry virutal environment:
    ```bash
    poetry shell
    ```

2. Before making any changes, stamp the database with the current revision:
    ```bash
    make stamp_db
    ```

3. Make your changes to the database models in `new_arrivals_chi/app/models.py`.

4. Generate a migration, you should see a new file in `new_arrivals_chi/migrations/versions/`:
    ```bash
    make create_revision
    ```

    Note that you may need to make changes to the migration file to ensure that the migration is correct.

5. Apply the migration to the database:
    ```bash
    make update_db
    ```

    The changes should now be reflected in the database.

# Using the Application

Below are video demonstrations for using the application from the perspective of 3 different users:

* [General User (Unauthenticated)](https://drive.google.com/file/d/1xjU0ppjwapJEmaTLxG063AfIdRWvKnnU/view?usp=drive_link)

* [Organization Admin (Permission to edit one assigned organization)](https://drive.google.com/file/d/1xXCtw5jmi7Xrotr2H7F3Tk49Dxy9mnpi/view?usp=sharing)

* [Admin (Permission to edit all organizations)](https://drive.google.com/file/d/1rc3HrA5umMv5SV2YZT4-4uHFoCCjvNaM/view?usp=sharing)

# Design and Values

This project is iterative, and centers  user is at the center of our design and implementation. 

Read more about our [design process](docs/design/README.md) and [project values](docs/values.md)

# Next Steps

This project is a work in progress, and we are excited to expand features and improve functionality in the near future.

Read our long term viability plan [here!](https://docs.google.com/document/d/1LIFzdIvIZWDqFrw0-qLcs_inXNo-YlhcOD7V58IhpW8/edit?usp=sharing)

# Authors

*   Federico Dominguez Molina
*   Aaron Haefner
*   Summer Long
*   Kathryn Link-Oberstar
*   Madeleine Roberts
*   Xiomara Salazar Flores

# License

This project is licensed under the [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) license.

# Acknowledgments

*   Thank you to our academic course advisors for this project James Turk and Michael Plunkett for support and guidance throughout this project.
*   Thank you to all the incredibly hardworking and amazing community organizations and individuals who generously dedicated their time to educate our team on the current status, needs, and challenges of new arrivals in Chicago, as well as provided valuable recommendations throughout the development of this project.
* Special thanks to:

    - City of Chicago - Office of Immigrants, Migrant, Refugee Rights: Marissa Arrez and Jesús Del Toro
    - Illinois Community for Displaced Immigrants: Johannes Favi
    - The Resurrection Project: Oswaldo Gomez, Laura Mendoza
    - Chicago Street Medicine: Saara-Anne Azizi, Dan Dolan

# Get in Touch

This project is a collaborative effort and we would love your feedback!

Have an idea to make it better? Submit feedback or report a bug [here.](https://forms.gle/T4gDc7fVu8GHCk2b6)

Want to get in touch? Email us at newarrivalschi.contact@gmail.com.
