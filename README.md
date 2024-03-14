# Project Setup Instructions

Follow these steps to get the project up and running on your local machine.

## Prerequisites

- Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

## Setup Instructions

1. **Clone the Repository**

   Clone the project repository to your local machine. Replace `REPO_URL` with the actual repository URL:

   ```bash
   git clone REPO_URL
Navigate to Project Directory

1. Change into the project directory:

  cd articles
  Create a Virtual Environment

2. Set up a Python virtual environment for the project. This creates an isolated environment for Python projects which can have their own dependencies, irrespective of what dependencies every other project has.


  python3 -m venv venv
  Activate the Virtual Environment

4. Activate the virtual environment:

  
  source venv/bin/activate
  On Windows, the command is slightly different:


  .\venv\Scripts\activate
  Install Django

Install Django using pip. This will install the latest version of Django:


  pip install django
  pip install django==5.0.2

Run the Development Server

Start the Django development server:


  python manage.py runserver
