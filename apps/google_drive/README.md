# Google Drive Search files.

### About:

This project is a simple flask app, where you'll be able to search files into the google drive api and list the existing files based in the search words you'll insert into the search field, also you are able to select file types to filter it. Download file is available, but  folder access is not available (Not enoght time)

### Get Google Drive API Credentials:

So first of all you'll need to create an app ***credentials*** to use this app, follow the official Google Drive Api Docs instructions: [Google Drive Credentials Download Instructions](https://developers.google.com/drive/api/quickstart/python?hl=en#set_up_your_environment "docs Google Drive Api")

Follow this instructions below, download your credentials.json and put it inside the `apps/google_drive` folder. Remember, should be named as `credentials.json` .

*Ps: Don't forget to enable your Google Drive API, without this you'll not be able to search files.*

### Running:

Run the command below:

```
flask --app main.py run --debug
```

With that, you'll be able to open [http:localhost:5000](). When you start the search and click in the search button or press enter, you'll be redirected to allow the app to access your google drive. Unless if your app is already in production mode, use the same account do you create the `credentials.json` .

After that you'll be able to search files.
