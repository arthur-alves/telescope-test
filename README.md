# How to install this project:

We highly recommend to use **Pyenv**:

Install Pyenv to manage different Python versions.

See documentation for installation in this link: [Pyenv Docs](https://github.com/pyenv/pyenv "Pyenv docs")

Please use Python version  `3.10.13`, for this use  this command to install pyenv specific version:

```
pyenv install 3.10.13
```

To install virtualenv, use this command:

```
~/.pyenv/versions/3.10.13/bin/pip install
virtualenv/.pyenv/versions/3.10.13/bin/virtualenv .venv
source .venv/bin/activate
```

After that, install the project itself:

```
pip install -r requirements.txt
```

And also, run this command bellow to install the Playwright browsers:

```
playwright install
```

### Apps of this project:

Now follow the app steps to run using link below:

[- Run Linkedin Scrapper](apps/linkedin/README.md "Linkedin Docs")

[- Run G2Crowd Crawler](apps/g2crowd/README.md "G2 Crawler Docs")

[- Run Google Drive Search APP](apps/google_drive/README.md "Google Drive Search Docs")
