from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from api.utils.dto import ScraperOutput, Quote
from api.utils.exceptions import ApiException


class GoodReadsContentProcessor:
    def __init__(self) -> None:
        pass

    def get_total_quote_count(self, content: str):
        try:
            count = content.split(sep=" ")[-1]
            processed_count = count.replace(",", "")
            return int(processed_count)
        except ValueError:
            return None

    def get_quote(self, content: str):
        return content.split("\n―")[0]

    def get_tags(self, content: str):
        try:
            tags = content[6:]
            processed_tags = tags.replace(" ", "")
            return processed_tags.split(",")
        except:
            return None

    def get_likes(self, content: str):
        try:
            likes = content.split(" ")[0]
            return int(likes)
        except ValueError:
            return None


class GoodReadsScraper:
    def __init__(
        self,
        driver: webdriver,
        url: str = "https://www.goodreads.com/quotes/tag/life",
        page: int = 1,
    ) -> None:
        self.page = page
        self.url = url + f"?page={self.page}"
        self.driver = driver
        self.content_processor = GoodReadsContentProcessor()
        self.output = ScraperOutput

    def scrape(self):
        self.driver.get(self.url)

        try:
            page_contents = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mainContent"))
            )

            total_quote_count_content = page_contents.find_element(
                By.CLASS_NAME, "mediumText"
            ).text
            total_quote_count = self.content_processor.get_total_quote_count(
                total_quote_count_content
            )

            quotes = []
            quote_blocks = page_contents.find_elements(By.CLASS_NAME, "quoteDetails")
            for quote in quote_blocks:
                quote_content = quote.find_element(By.CLASS_NAME, "quoteText").text
                quote_content = self.content_processor.get_quote(quote_content)

                author = quote.find_element(By.CLASS_NAME, "authorOrTitle").text

                tags_content = quote.find_element(
                    By.CLASS_NAME, "greyText.smallText.left"
                ).text
                tags = self.content_processor.get_tags(tags_content)

                likes_content = quote.find_element(By.CLASS_NAME, "right").text
                likes = self.content_processor.get_likes(likes_content)

                quotes.append(
                    Quote(quote=quote_content, author=author, tags=tags, likes=likes)
                )

            self.output.total_quote_count = total_quote_count
            self.output.quotes = quotes
            return self.output

        except NoSuchElementException:
            raise ApiException.FedWrongURL(
                context={
                    "message": "The scraper does not currently have provisions to work on this URL"
                }
            )
