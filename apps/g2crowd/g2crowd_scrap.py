import asyncio
import csv
import json
import os
import random

from playwright.async_api import async_playwright

from apps.utils.utils import alert, get_csv_content_list, success, warning

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.38",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edg/93.0.961.38",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edg/93.0.961.38",
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_csv():
    csv_file_path = os.path.join(APP_PATH, "csv_in/g2crowdurls.csv")
    rows = get_csv_content_list(csv_file_path)
    return rows


async def check_robot_bypass(page):
    warning("CHECKING HUMAN ACCESS")
    challenge = await page.query_selector("#challenge-running")

    if not challenge:
        success("Pass")
        return None
    await page.wait_for_selector("iframe")

    iframe_element = await page.query_selector("iframe")
    if iframe_element:
        iframe = await iframe_element.content_frame()
        warning("GETTING IFRAME")
        await iframe.wait_for_selector("input[type=checkbox]")
        success("BY PASS CHALLENGE")

        checkbox_element = await iframe.query_selector("input[type=checkbox]")

        if checkbox_element:
            await checkbox_element.click()


async def get_page_content(page, url):
    await page.goto(url)
    await check_robot_bypass(page)
    await page.wait_for_selector(".product-head__title")
    content = await get_content(page)
    await page.close()

    return content


async def scrape_g2_reviews():
    company_info = []
    async with async_playwright() as p:
        show_browser = (
            False if os.environ.get("SHOW_BROWSER", "").lower() == "true" else True
        )
        browser = await p.chromium.launch(headless=show_browser)

        rows = get_csv()
        if not rows:
            alert("CSV File Empty. [STOP]")
            return None
        task_list = []
        for url in rows:
            # We need to use different random user agent to simulate random browsers to avoid block
            context = await browser.new_context(user_agent=get_random_user_agent())
            page = await context.new_page()
            task_list.append(get_page_content(page, url[0]))

        # Avoid CPU overload
        step = int(os.environ.get("MAX_PAGES"))
        for t in range(0, len(task_list), step):
            batch_result = task_list[t : t + step]
            company_info.extend(await asyncio.gather(*batch_result))

        await browser.close()

    await write_to_json(company_info)


async def write_to_json(data: list[list]) -> None:
    file_name = os.path.join(APP_PATH, "json_out/g2crow.json")

    with open(file_name, "w", newline="") as csv_file:
        csv_file.write(json.dumps(data, indent=4))

    success(f"[DONE] - File saved on path: {file_name}")


async def get_content(page):
    title_element = await page.query_selector(".product-head__title a")
    title = await title_element.inner_html()
    reviews_element = await page.query_selector(
        ".product-head__title .star-wrapper__desc ul li a"
    )
    review_count = await reviews_element.inner_text()
    description_element = await page.query_selector(".paper .paper--nestable")
    description = await description_element.inner_text()
    return {"title": title, "review_count": review_count, "description": description}
