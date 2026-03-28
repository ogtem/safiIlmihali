import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load the HTML file
        file_path = f"file://{os.path.abspath('risale_final.html')}"
        print(f"Loading {file_path}")
        await page.goto(file_path)

        # First add a highlight by mocking localStorage
        await page.evaluate('''() => {
            const h = [{
                id: "test1",
                text: "Bismillah",
                timestamp: Date.now()
            }, {
                id: "test2",
                text: "Elhamdu lillahi rabbi",
                timestamp: Date.now() - 100000
            }];
            localStorage.setItem("userHighlights", JSON.stringify(h));
            // reload to apply highlights
        }''')

        await page.reload()

        # Wait for marks to appear
        await page.wait_for_selector('mark.user-highlight')

        # Open highlights list
        await page.click('#highlightsBtn')

        # Wait for modal to be visible
        await page.wait_for_selector('#highlightsModal.open')

        # Verify items in list
        items = await page.locator('.hl-item').all()
        print(f"Found {len(items)} highlight items in modal.")

        if len(items) == 2:
            print("Successfully verified highlights list items.")

        # Take a screenshot
        os.makedirs('/home/jules/verification', exist_ok=True)
        await page.screenshot(path='/home/jules/verification/highlights_list.png')

        # Click an item to test scrolling
        await items[0].click()

        # Verify modal closes
        is_hidden = await page.evaluate('!document.getElementById("highlightsModal").classList.contains("open")')
        print(f"Modal is closed after click: {is_hidden}")

        await browser.close()

asyncio.run(run())
