# How to install this project:

We highly recommend to user **Pyenv**:

Install PyEnv to manage different Python versions

See documentation for installation: [Pyenv Docs](https://github.com/pyenv/pyenv "Pyenv docs")

Please user Python version  3.10.13, run this command after install pyenv:

```
pyenv install 3.10.13
```

To install virtualenv, use this command:

```
~/.pyenv/versions/3.10.13/bin/pip install
virtualenv/.pyenv/versions/3.10.13/bin/virtualenv .venv
source .venv/bin/activate
```

After that install the project itself:

```
pip install -r requirements.txt
```

And after run this command to install the Playwright browser:

```
playwright install
```

Now follow the app steps to run using link below:

[Run Linkedin Scrapper](apps/linkedin/README.md "Linkedin Docs")
