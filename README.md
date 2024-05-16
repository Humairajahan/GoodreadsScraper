# GoodReadsScraper

### Features

- [x] Scrape quotes from Goodreads. Wrapped up in an API.
- [x] Store the scraped contents along with their metadata in a postgres database.
- [x] Database populate call handling via a background task.
- [x] Database volume kept persistent 
- [x] The UI for the database (pgadmin) volume also kept persistent
- [x] API for retrieving most liked quotes. Allows for the following features:
  - [x] Filter by tags
  - [x] Filter by author 
  - [x] Sort by like amount
  - [x] Search in quotes
  - [x] Pagination


### Future scope

- [ ] Currently only allows for filtering by single tag. Can be extended to filtering by multiple tags.
- [ ] Currently not following best practice and maintain an env file to store sensitive information.


### Run

Make sure you have docker installed in your system.

```python
docker compose up --build -d
```
