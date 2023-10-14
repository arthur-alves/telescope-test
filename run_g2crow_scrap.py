import asyncio

from dotenv import load_dotenv

load_dotenv()
from apps.g2crowd.g2crowd_scrap import scrape_g2_reviews

asyncio.run(scrape_g2_reviews())
