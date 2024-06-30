# lyrical

lyrical is a dynamic web application designed for music enthusiasts. Built with Flask, it offers a platform for users to explore, create, and manage their music playlists. It integrates seamlessly with a MySQL database to store user information and song details, ensuring a personalized music experience.

## Features

-   **User Authentication**: Secure login and signup functionalities for users.
-   **Music Library**: Access to a vast library of songs, including free songs and user-created playlists.
-   **Playlist Management**: Users can create, modify, and delete their playlists.
-   **Song Upload**: Admins have the ability to upload new songs to the library.
-   **Dynamic Music Player**: A built-in music player that allows users to listen to songs directly from their playlists.

## Functions

-   `signup()`: Handles user registration.
-   `login()`: Manages user login.
-   `scan_free_songs()`: Scans and imports free songs into the database.
-   `scan_all_songs()`: Scans and imports all songs into the database.
-   `upload_song()`: Allows admins to upload new songs.

## Getting Started

To get lyrical running on your machine, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/monishbl/Music_Player---DBMS_Project.git
    cd lyrical
    ```

2. **Set Up the Database**

    Ensure MySQL is installed and running on your machine. Create a database and update the credentials in `connect.py`:

    ```py
    mydb = mysql.connector(
        host="localhost",
        user="<Your_Username>",
        passwd="<Your_Password>",
        database="<Your_Database_Name>",
        auth_plugin='mysql_native_password'
    )
    ```

3. **Install Dependencies**

    ```bash
     python -m venv env
    source env/bin/activate  # Unix/MacOS
    source env/Scripts/activate  # Windows
    pip install -r requirements.txt
    ```

4. **Generate Tailwind CSS**

    ```bash
    npm install
    npx tailwindcss -i ./static/input.css -o ./static/output.css --watch
    ```

5. **Run the Application**

    ```bash
    python app.py
    ```

License
-------
lyrical is licensed under the MIT License. See the LICENSE file for more details.