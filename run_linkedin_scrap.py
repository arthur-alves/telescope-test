import asyncio

from dotenv import load_dotenv

load_dotenv()

from apps.linkedin.search_companies import main

asyncio.run(main())
