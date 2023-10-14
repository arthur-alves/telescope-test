import asyncio
import csv
import os

from playwright.async_api import async_playwright

from apps.utils.utils import alert, get_csv_content_list, success, warning

COMPANIES_LIST = []
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_csv_search_list():
    csv_file_path = os.path.join(APP_PATH, "csv_in/companies.csv")
    rows = get_csv_content_list(csv_file_path)
    if not rows:
        alert("CSV File Empty. [STOP]")
        return None

    columns_count = len(rows[0])
    if columns_count > 1:
        warning("Your Columns:\n", rows[0], "\n...", "\n")
        column = input(
            f"We have {columns_count} columns in this CSV. Starting from 1, which column we are located the company names?"
        )
        column_selected = False
        while not column_selected:
            try:
                column = int(column)
                if column <= columns_count and column > 0:
                    column_selected = True
                    break
            except ValueError:
                alert("This value is not valid. please re-enter your choice.")
            column = input(f"Please select the between 1 to {columns_count}.")
    else:
        column_selected = 1

    for row in rows:
        COMPANIES_LIST.append(row[column_selected - 1])
    success("COMPANIES LIST DONE:", COMPANIES_LIST)


async def write_to_csv(data: list[list]) -> None:
    file_name = os.path.join(APP_PATH, "csv_out/companies_result.csv")

    with open(file_name, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the data to the CSV file
        for row in data:
            csv_writer.writerow(row)
    success(f"[DONE] - File saved on path: {file_name}")


async def main():
    try:
        get_csv_search_list()
    except FileNotFoundError:
        alert("Ops! File Not found")
        return
    async with async_playwright() as p:
        show_browser = (
            False if os.environ.get("SHOW_BROWSER", "").lower() == "true" else True
        )
        browser = await p.chromium.launch(headless=show_browser)
        context = await browser.new_context(user_agent=USER_AGENT)
        page = await context.new_page()
        await login(page)
        await find_companies_by_csv(context)
        # Close the browser
        await browser.close()


async def login(page) -> None:
    await page.goto("https://www.linkedin.com/login/")
    await page.fill('input[type="text"]', os.environ.get("LINKEDIN_EMAIL"))
    await page.fill('input[type="password"]', os.environ.get("LINKEDIN_PASS"))

    # Click the "Sign in" button
    await page.click('button[type="submit"]')

    # Wait for the login to complete
    await page.wait_for_url("https://www.linkedin.com/feed/")


async def find_companies_by_csv(context) -> None:
    if not COMPANIES_LIST:
        raise ValueError(
            "Companies List is empty. Please check the csv file inside the csv_in folder."
        )

    companies_urls = []
    task_list = []
    for company in COMPANIES_LIST:
        task_list.append(get_content(context, company))

    # Avoid CPU overload
    step = int(os.environ.get("MAX_PAGES"))
    for t in range(0, len(task_list), step):
        batch_result = task_list[t : t + step]
        companies_urls.extend(await asyncio.gather(*batch_result))
    success("Writing to CSV")
    await write_to_csv(companies_urls)


async def get_content(context, company):
    page = await context.new_page()
    await page.goto(
        f"https://www.linkedin.com/search/results/companies/?keywords={company}"
    )
    await page.wait_for_selector("div.search-results-container")

    first_result = await page.query_selector("li.reusable-search__result-container")
    link = await first_result.query_selector("a")
    link_url = await link.get_attribute("href")

    success(f"Get first search result of company named {company} on link: {link_url}")
    company_fetched = await get_total_employees(page, link_url)
    success(f"Got employees from company {company}: {company_fetched}")
    await page.close()
    return [company] + company_fetched


async def get_total_employees(page, company_url: str) -> None:
    await page.goto(company_url)
    await page.wait_for_selector("div.org-top-card-summary-info-list")
    employees_link = await page.query_selector(
        "a.org-top-card-summary-info-list__info-item"
    )
    total_employees = await employees_link.inner_text()
    return [company_url, total_employees]
