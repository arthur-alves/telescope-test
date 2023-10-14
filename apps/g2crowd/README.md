# How to run G2Crowd crawler.

### Explanation about the project:

This crawler get some contents from g2.com based in a CSV with the urls. It uses random user-agent to avoid being blocked by cloudflare used in g2.com, if it shown the script will be able to detect and solve the captcha challenge.

#### How to run:

Set the `.env` in the root of the project:

```
MAX_PAGES=5 # numbers of max pages used by playwright to avoid cpu overloads. It will run asyncronous
SHOW_BROWSER=False #If you don't want to show the browser process
```


Put the CSV with g2crowd urls inside the `apps/g2crowd/csv_in/` folder. If your csv have more than one column, the script will ask to you the correct column to start the scrapper.

After that run the command below:

```
python run_g2crow_scrap.py
```

At the end, will be able to check the results in json format stored in apps/g2crowd/json_out
