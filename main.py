import io

from flask import Flask, render_template, request, send_file

from apps.google_drive.gdrive import gdrive_api

app = Flask(__name__)


@app.route("/")
def google_drive():
    search = request.args.get("search")
    mime = request.args.get("mime-type")
    files = []

    if search or mime:
        files = gdrive_api.search_files(search, mime)
    return render_template("google-drive.html", files=files, mime=mime, search=search)


@app.route("/download")
def download_file():
    file_id = request.args.get("file_id")
    drive_service = gdrive_api.create_drive_service()
    file = drive_service.files().get(fileId=file_id).execute()
    file_name = file["name"]
    request_file = drive_service.files().get_media(fileId=file_id)
    content = request_file.execute()

    response = send_file(
        io.BytesIO(content), as_attachment=True, download_name=file_name
    )
    return response
