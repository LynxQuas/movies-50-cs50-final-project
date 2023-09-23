   # Movie 50 ( CS50 final project )

#### Video Demo: https://www.youtube.com/watch?v=uA9-uyhUvNs

#### Description:
    Movie 50 is a web application designed as the final project for CS50. It provides users with a comprehensive platform for exploring and discovering movies and TV shows. With Movie 50, users can easily access trending content, search for specific titles, view in-depth information about movies and TV shows, and even save their favorite selections to their account for future reference.

## Table of Contents

-[Project Name](#project-name)

-[Table of Contents](#table-of-contents)

-[Description](#description)

-[Prerequisites](#prerequisites)

-[Usages](#usage)

-[Features](#features)

-[Contributing](#contributing)

## Prerequisites
Prerequisites
Before diving into Movie 50, make sure you have the following prerequisites in place:

Python 3.7 or Higher: Movie 50 is built on Python, and it requires Python 3.7 or a higher version to run effectively.

Flask (Python Web Framework): Flask is used to create the web application and handle HTTP requests. Ensure you have Flask installed.

SQLite Database: Movie 50 relies on an SQLite database to store user data and favorites. Make sure SQLite is set up and configured.

JavaScript: JavaScript is used for dynamic interactions within the application. Ensure that JavaScript is enabled in your browser.

The Movie Database (TMDb) API Key: Movie 50 fetches movie and TV show data from TMDb. You'll need to obtain an API key from TMDb to access their data.

Now that we've covered the prerequisites, let's move on to installing and using Movie 50.

## Installation
To set up Movie 50 on your local machine, follow these steps:
 1. Clone the Repository: Begin by cloning the Movie 50 repository to your local system using Git.
 2. Install Dependencies: Navigate to the project directory and install the required Python dependencies using pip.
 3. Obtain a TMDb API Key: Visit The Movie Database (TMDb) website (https://www.themoviedb.org/) and create an     account if you don't already have one. Once logged in, navigate to your account settings and generate an API key. Copy this API key for later use.
    

## Features
   - ### Trending Movies and TV Shows: 
     On the home page, Movie 50 displays trending movies and TV shows sourced from The Movie Database (TMDb) API. Stay up-to-date with the latest in the world of entertainment.

   - ### Search Functionality: 
     Movie 50 offers a powerful search feature. Users can search for specific movies and TV shows by entering keywords into the search bar. The application seamlessly fetches search results from the TMDb API, making it easy to find what you're looking for.

    - ### View Details: 
     Get all the details you need about individual movies and TV shows. Access information such as title, rating, poster, and media type (movie or TV show) to make informed choices.

    - ### Save Favorites: 
     Registered users have the option to save their favorite movies and TV shows directly to their account. These favorites are securely stored in the SQLite database, ensuring you never lose track of your preferred content.

    - ### Change Password: 
     Registered users can update their account password, adding an extra layer of security and convenience to their Movie 50 experience.

## Usage
Follow these simple steps to get started with Movie 50:

1. Start the Flask application:
2. Open your web browser and navigate to http://localhost:5000.
3. You can now use the web application to:
    - View trending movies and TV shows on the home page.
    - Search for specific movies and TV shows using the search bar.
    - View details about individual movies and TV shows.
    - Save your favorite movies and TV shows to your account.
    - Update your account password.

## Contributing
    We welcome contributions from the community! If you're interested in contributing to this project, please follow these steps:

    1. Fork the repository.
    2. Create a new branch for your feature or bug fix.
    3. Make your changes and commit them.
    4. Push your changes to your forked repository.
    5. Create a pull request to the original repository.