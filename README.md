## New Arrivals Chi

New Arrivals Chi seeks to address the common challenges encountered by newly arrived individuals in Chicago. Such individuals often find themselves struggling with the complexities of accessing essential resources, from navigating systems to staying updated on what's available. This project hopes to ease these difficulties and support the newly arrived community by establishing am online platform tailored to their needs.

Through this portal, we aim to offer guidance on task prioritization and provide the latest information regarding vital services. Our current focus areas are medical care, food assistance, and legal support.

## Getting Started

Follow these instructions to get the project running on your computer for development and testing.

### Table of Contents

1.  Prerequisites
    1.  Project Structure
    2.  Installing
    3.  Running the Project
    4.  Running the Tests
2.  Authors
3.  License
4.  Acknowledgments

## Prerequisites

_To be updated later with requirements for the software and other tools in the upcoming weeks._  

### Project Structure 
*   `.github/`: This folder contains the templates and workflows for our github repository.
*   `docs/`: This folder contains documents outlining decisions made throughout the development process.
    * `decisions/`: This folder contains the decisions made regarding the various application components.
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

## Authors

*   Federico Dominguez Molina
*   Aaron Haefner
*   Summer Long
*   Kathryn Link-Oberstar
*   Madeleine Roberts
*   Xiomara Salazar Flores

## License

This project is licensed under the [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) license.

## Acknowledgments

*   Thank you to our academic course advisors for this project James Turk and Michael Plunkett for support and guidance throughout this project.
*   Thank you to all the incredibly hardworking and amazing community organizations and individuals who generously dedicated their time to educate our team on the current status, needs, and challenges of new arrivals in Chicago, as well as provided valuable recommendations throughout the development of this project.
