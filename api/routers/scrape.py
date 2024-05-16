from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from api.utils.dto import ScrapeIn, ScrapeOut
from api.utils.setup_driver import Driver, webdriver
from api.utils.scraper import GoodReadsScraper
from api.utils.populate import Populate

router = APIRouter()


@router.post("/scrape", response_model=ScrapeOut, status_code=status.HTTP_200_OK)
async def scrape(
    request: ScrapeIn,
    db_update_call: BackgroundTasks,
    driver: webdriver = Depends(Driver().get_driver),
):
    try:
        goodreads = GoodReadsScraper(driver=driver, url=request.url, page=request.page)
        scraped_content = goodreads.scrape()
        db_update_call.add_task(Populate().populate, scraped_content)
        return scraped_content
    except Exception as e:
        raise HTTPException(status_code=int(e.status_code), detail=e.context["message"])
