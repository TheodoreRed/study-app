# Study Flashcard App

This is a Django-based backend for a Study Flashcard application. The application allows users to create, retrieve, update, and delete study sets and flashcards. This backend is ready to be integrated with a frontend application built with JavaScript, React or any other technology that can consume a RESTful API.

## Features
- **User Authentication**: The application provides robust user authentication features. This includes registration, login, and logout capabilities. Users can also change their passwords and reset them if they forget.

- **Study Set Management**: Users can create study sets, which serve as categories or topics for flashcards. Each study set can have a title and description. Users can view all their study sets, update them, and delete them when they are no longer needed.

- **Flashcard Management**: Within each study set, users can create individual flashcards. Each flashcard has a term and a definition. Like study sets, users can view all their flashcards, update them, and delete them.

## API Endpoints

This project uses Django Rest Framework and Djoser for User Authentication. Below are the endpoints for the application:

### User Authentication (Djoser)

- `/auth/` - User registration, login and logout
- `/auth/users/` - Provide username and password in POST to create a new user account
- `/auth/login/` - Log in a user
- `/auth/logout/` - Log out a user/ invalidates their authentication token
- `/auth/password/reset/` - Request a password reset
- `/auth/password/reset/confirm/` - Confirm a password reset
- `/auth/password/change/` - Change a user's password

### Auth Tokens (Djoser)

- `/auth/token/` - Token management
- `/auth/token/create/` - Create a new auth token
- `/auth/token/verify/` - Verify an auth token
- `/auth/token/refresh/` - Refresh an auth token

### Study Sets & Flashcards

- `/api/studysets/` - Get all study sets for the authenticated user
- `/api/studysets/<id>/` - Get, update or delete a specific study set
- `/api/flashcards/` - Get all flashcards for the authenticated user
- `/api/flashcards/?study_set=<study_set_id>` - Get all flashcards for a specific study set for the authenticated user.
- `/api/flashcards/<id>/` - Get, update or delete a specific flashcard

## Setup & Installation


## Tech Stack

- Python
- Django
- Django Rest Framework
- Djoser
- MySQL

## Future Work
1. Set up React app
