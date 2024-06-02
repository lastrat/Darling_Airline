# Darling Airlines
Welcome to the Darling Airline Flight Management System! This system is designed to streamline and manage all aspects of flight operations for Darling Airline, providing an efficient and user-friendly interface for both airline staff and passengers.
## Overview
The Darling Airline Flight Management System is a web application designed to streamline the management of flight operations and reservations. It provides functionalities for both passengers and airline staff, ensuring efficient handling of flight schedules, bookings, and customer information.

## System Requirements
* Operating System: Windows 10 or later, macOS 10.12 or later, Linux
* Processor: Intel i7 or equivalent
* Memory: 8 GB RAM
* Storage: 500 MB of free space
* Database: PostgreSQL
* Language: Python (Django)
* Browser: Latest version of Chrome, Firefox, Safari, or Edge

## Features
- User registration and authentication
- Flight booking
- Viewing and managing reservations
- Administrative panel for managing flights, airplanes, and reservations
- Boarding pass generation
- Real-time flight status updates

## Installation

### Prerequisites

Ensure you have the following software installed:

- Python 3.x
- Django
- pip (Python package installer)

### Steps

1. **Clone the repository:**
   ```sh
   git clone [https://github.com/your-username/darling-airline.git](https://github.com/lastrat/Darling_Airline.git)
   cd darling-airline

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt

4. **Restore the database:**
   First create an empty postgres database named __darling_airline__
   ```sh
   python manage.py restore_db darling_airline_backup.sql
  
5. **Run the development server:**
   ```sh
   python manage.py runserver

## Usage
### Accessing the Application
* __User Portal:__ Visit http://127.0.0.1:8000/ to access the user-facing portal.
* __Admin Portal:__ Visit http://127.0.0.1:8000/admin to access the administrative panel.

### User Authentication
* Users can register and log in to search for flights, book tickets, and manage their reservations.
* Admin users can log in to the admin panel to manage flights, airplanes, and reservations.

## Technologies Used
* __Backend:__ Django
* __Frontend:__ HTML, CSS, JavaScript
* __Database:__ PostgreSQL
* __Other:__ Bootstrap

## Contributing
We welcome contributions to Darling Airline Flight Management System. To contribute, follow these steps:
1. Fork the repository.
2. Create a new branch: **git checkout -b feature-branch**
3. Make your changes and commit them: **git commit -m 'Add new feature'**
4. Push to the branch: **git push origin feature-branch**
5. Create a pull request describing your changes.

## Contact
For questions or support, please contact us from our various github account
Thank you for using Darling Airline Flight Management System!
