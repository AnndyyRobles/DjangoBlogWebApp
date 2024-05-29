# My Blog
## Overview
My Blog is a web application built with Django, designed for creating and managing blog posts. Users can register, log in, create, edit, and delete posts, as well as comment on them. The application uses PostgreSQL for database management and emphasizes security and responsive design.

## Features
User Authentication: Register, log in, and log out securely.
Post Management: Create, edit, delete, and view blog posts.
Comments: Comment on blog posts.
Responsive Design: Optimized for various screen sizes.
Security: Environment variable management for sensitive data.

## Installation
Prerequisites
Python 3.x
pip (Python package installer)
virtualenv (recommended)

## Setup
### Clone the repository:
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

### Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install the dependencies:
pip install -r requirements.txt

### Apply migrations:
python manage.py migrate

### Create a superuser (optional but recommended for accessing the admin panel):
python manage.py createsuperuser

### Run the development server:
python manage.py runserver

### Open your browser and go to http://127.0.0.1:8000/ to see the application in action.

## Usage
Creating Posts: Log in and navigate to the "Create Post" page.
Editing Posts: Go to a post and click "Edit".
Deleting Posts: Go to a post and click "Delete".
Commenting: Enter a post and submit a comment.

## Acknowledgments
Developed by [Your Name].
