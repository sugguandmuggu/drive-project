## Table of Contents

- [Landing Page](#landing-page)
- [API Endpoints](#api-endpoints)
  - [Login](#login)
  - [Callback](#callback)
  - [Drive Upload](#drive-upload)
  - [Drive Download](#drive-download)
  - [Drive List Files](#drive-list-files)
- [Chat App](#chat-app)
 
## Landing Page

- Go to `https://driveproject-a525e7ef0526.herokuapp.com/` for the landing page

## API Endpoints

### Login

- **Endpoint**: `/auth/login/`
- **Method**: `GET`
- **Description**: Redirects to Google login page.

#### How to use

1. Open your browser and navigate to `https://driveproject-a525e7ef0526.herokuapp.com/`.
3. You will be redirected to the landing page. Click on login.
4. After logging in, you will be redirected back to the callback endpoint.

### Callback

- **Endpoint**: `/auth/callback/`
- **Method**: `GET`
- **Description**: Handles the callback from Google after login.

#### How to use

1. This endpoint is automatically called after a successful login via the Google login page.
2. It processes the authentication response and retrieves the access token.

### Drive Upload

- **Endpoint**: `/drive/upload/`
- **Method**: `POST`
- **Description**: Uploads files to Google Drive.

#### How to use in Postman

1. Open Postman.
2. Create a new `POST` request.
3. Set the URL to `https://driveproject-a525e7ef0526.herokuapp.com/drive/upload/`.
4. Go to the `Body` tab and select `form-data`.
5. Add a new key `file` and set the type to `File`.
6. Choose the file you want to upload.
7. Click `Send`.

### Drive List Files

- **Endpoint**: `/drive/list-file/`
- **Method**: `GET`
- **Description**: Lists files from Google Drive.

#### How to use in Postman

1. Open Postman.
2. Create a new `GET` request.
3. Set the URL to `https://driveproject-a525e7ef0526.herokuapp.com/drive/list-file/`.
4. Add query parameters:
    - `query`: The search query string.
    - `mimeType`: The MIME type of the files to list.
5. Click `Send`.

### Drive Download

- **Endpoint**: `/drive/download-file/`
- **Method**: `GET`
- **Description**: Downloads files from Google Drive.

#### How to use in Postman

1. Open Postman.
2. Create a new `GET` request.
3. Set the URL to `https://driveproject-a525e7ef0526.herokuapp.com/drive/download-file/`.
4. Add a query parameter `file_id` with the ID of the file you want to download.
5. Click `Send`.

## Chat App

The `chat_app` provides real-time chat functionality within the DriveProject. Below are the details on how to use the chat app.

### Usage

1. **Access the chat app**:
    - Open your browser and navigate to ``https://driveproject-a525e7ef0526.herokuapp.com/chat/<room-name>``.
2. **Send and receive messages**:
    - Once in a chat room, you can send and receive messages in real-time.



**Author**: Saksham Jaiswal  
**Email**: jaiswalsaksham32@gmail.com

