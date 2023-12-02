# Todo List Flask App

This is a simple Todo List Flask application with MongoDB integration for user authentication and task management.

## Setup

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up your environment variables. Create a `.env` file in the root directory with the following variables:

    ```env
    MONGO_DB=your_mongo_db_connection_string
    SECRET_KEY=your_secret_key
    ```

3. Run the application:

    ```bash
    python app.py
    ```

The application will be running on `http://localhost:5000`.

## Endpoints

### https://www.postman.com/joint-operations-administrator-82737956/workspace/revou/documentation/28997654-11f81b3a-602d-4f65-936f-0a1d2f603bab
  
## Struktur Folder

- **controllers**: Berisi kontroler untuk mengelola logika bisnis.
- **middleware**: Berisi middleware, seperti VerifyToken, yang digunakan di aplikasi.
- **models**: Berisi definisi model data, seperti User dan Task.
- **routes**: Berisi rute aplikasi, terpisah berdasarkan fungsionalitasnya.


## Technology Stack

- **Frontend** : React.js, Material-UI, Redux, Formik, Yup
- **Backend** : Python Flask
- **Database** : MongoDB (Refer to your backend README.md for more details)
- **Authentication** : JWT Tokens


## Contributing
Contributions are welcome! If you find a bug or want to add a new feature, please create an issue or a pull request.

## Author
Restu Windri Pangestu

## Lisensi

MIT License