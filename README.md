# Tyres_App
 
## Introduction

### What is this project about?

Develop a web app for tyre engineers to manage and track tyre sets for car races. Engineers input the number of tyre sets per type (Soft, Medium, Hard) available for each weekend. They also define the race weekend's sessions (e.g., Free Practice, Qualifying, Race) and specify the number of sets to return after each session except the Race. The app should allow saving these settings for recurring race formats.

The main feature includes planning the tyre usage per session, deciding which sets to return, and visualizing remaining sets for the Race. The app tracks each set's state, indicating whether they are new or used. This tool aims to optimize tyre management during race weekends.
This project is designed to manage the states and data related to different sets of tyres. Additionally, it provides functionalities to manage weekend formats and sessions. The application consists of a frontend and a backend, both of which are containerized using Docker.

### Deployment Instructions

#### Using Docker Compose

1. Clone the repository to your local machine.
2. Navigate (`cd`) to the directory containing the `docker-compose.yaml` file.
3. Run `docker-compose up`.
4. Access the frontend at [http://localhost:3000/](http://localhost:3000/).

For backend-specific tests, you can use port 8000: [http://localhost:8000/](http://localhost:8000/).

#### API Endpoints for Testing

1. **Tyre Sets**
    - [GET] [http://127.0.0.1:8000/api/tyre_sets/](http://127.0.0.1:8000/api/tyre_sets/): View all tyre states.
    - [GET] [http://127.0.0.1:8000/api/tyre_sets/<id>/](http://127.0.0.1:8000/api/tyre_sets/<id>/): View the state of a specific tyre set by ID.
    - [PUT] [http://127.0.0.1:8000/api/tyre_sets/<id>/](http://127.0.0.1:8000/api/tyre_sets/<id>/): Modify parameters of a specific tyre set by ID.

2. **Weekend Format**
    - [GET] [http://127.0.0.1:8000/api/weekend_format/](http://127.0.0.1:8000/api/weekend_format/): View counts of three types of tyres for the weekend.
    - [POST] [http://127.0.0.1:8000/api/weekend_format/](http://127.0.0.1:8000/api/weekend_format/): Add a new weekend object.

3. **Weekend Session**
    - [GET] [http://127.0.0.1:8000/api/weekend_session/](http://127.0.0.1:8000/api/weekend_session/): View all session data.
    - [POST] [http://127.0.0.1:8000/api/weekend_session/](http://127.0.0.1:8000/api/weekend_session/): Add a new session object.

4. **Weekend Templates**
    - [POST] [http://127.0.0.1:8000/api/weekend_format/save_weekend_template/](http://127.0.0.1:8000/api/weekend_format/save_weekend_template/): Save the current weekend format and session objects as a template.
    - [GET] [http://127.0.0.1:8000/api/weekend_template/](http://127.0.0.1:8000/api/weekend_template/): View all saved templates.
    - [POST] [http://127.0.0.1:8000/api/weekend_format/apply_weekend_template/](http://127.0.0.1:8000/api/weekend_format/apply_weekend_template/): Apply the selected template data (not fully debugged).

5. **Data Management**
    - [POST] [http://127.0.0.1:8000/api/weekend_format/clear_all_data/](http://127.0.0.1:8000/api/weekend_format/clear_all_data/): Clear all data, including templates.
    - [POST] [http://127.0.0.1:8000/api/weekend_format/clear_all_data_keepTemplate/](http://127.0.0.1:8000/api/weekend_format/clear_all_data_keepTemplate/): Clear all data except for templates (not fully debugged).
## Project Advantages

### Easy Deployment with Docker Compose

The use of Docker Compose simplifies the deployment process. It enables you to set up both the frontend and backend by running a single command, making the setup effortless.

### Enhanced Security with Dual Validation

Both the frontend and backend validate input data, providing an extra layer of security.

1. The backend has safeguards to restrict the number of tyres that can be returned.
2. The frontend performs additional calculations on numerical inputs to ensure the correct number of tyres is used in each race session.

### Relational Database

The application uses a relational database and object-oriented programming (OOP) for better data management.

1. Data is stored as object properties, which are interconnected through foreign keys and many-to-many relationships, providing clear logic and better data integrity.

### RESTful API

The connection between the frontend and backend adheres to RESTful API standards, offering better compatibility and stability.

### Simple and Direct Operational Logic

The application is designed to be user-friendly. It has a straightforward interface and workflow, making it easy to understand and use.

### Scalability

1. Comprehensive Data Model: The data model includes entities like 'car' and 'race weekend,' allowing for future extensions, such as multi-team management and multiple weekend management.
2. Technology Stack: The application uses a React+Django stack, which can handle most production environments and offers excellent scalability, both in terms of size and features.
## Potential Issues and Future Directions

### Data Relationship Optimization

1. Due to the time constraints of rapid development, some models are not fully utilized. With more time, the relationships between models, especially many-to-many relationships, should be optimized for better data integrity.

### Authentication and User Management

1. Although the backend API adheres to RESTful API standards, token-based authentication should be added if time allows.
2. A login system is required for team and multi-user management. This will likely involve adding a new data model for 'User' and more extensively utilizing the 'Car' model to manage multiple vehicles.

### Error Handling

1. Limited time has not allowed for comprehensive error handling mechanisms, such as try-catch, to be implemented in both the frontend and backend.

### Testing

1. More comprehensive testing, including unit tests focused on model and view behaviors, and integration tests involving various API requests and static file loading, should be conducted.
2. Load testing should also be considered if the software is to be used by multiple teams.

### Deployment

1. While Docker Compose is currently used for local deployment, cloud-based deployment should be considered for broader access across different devices like smartphones and iPads.

### Code Quality

1. The code was mostly written to meet quick development needs, resulting in redundancy and sub-optimal readability.
2. The current code has not undergone performance auditing in terms of time and space complexity. A thorough review should be conducted if it is to be used in production.

### Template Feature

1. The template feature is not fully developed yet. Although the backend APIs related to templates are mostly done, the frontend lacks a stable 'Apply Template' function.

### UI/UX Enhancements

1. The interface is functional but not optimized for user interaction.
2. Device-specific UI improvements are needed, especially for mobile devices. One idea is to use a stack-based interface for each tyre ID, allowing detailed configurations in a sub-page.

### Backup System

1. The current database is SQLite, which may not be adequate for production needs. A robust backup strategy or migration to a cloud-based database service may be necessary.
