# Linkeding Company Crawler

### About:

This app intent to crawler some linkedin company info based in a csv file with the company names and save the result as csv with columns with company name, url and employees count.

### Running:

To run linkedin company scrap, first we need to config `.env `file, *(don't worry .env is not watched by repo)* create it at the root of the project.
Copy all content from .env.example and create your fill the variables like below:

```shell
LINKEDIN_EMAIL='<linkedin email>'
LINKEDIN_PASS='linkedin_password'
MAX_PAGES=5 # numbers of max pages used by playwright to avoid cpu overloads. It will run asyncronous
SHOW_BROWSER=False #If you don't want to show the browser process
```

*PS: Use a linkedin default login using email and password, do not use it with secutiry issues enabled like two factor and another kind of authentication.*

Put the CSV with company names inside the `apps/linkedin/csv_in/` folder. If your csv have more than one column, the script will ask to you the correct column to start the scrapper.

Run this command below after inserted the csv:

```
python run_linkedin_scrap.py
```

At the end of the script, you'll be able to see the full path where the results has been saved.
