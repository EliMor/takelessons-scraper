# Scrape the chat logs from TakeLessons

## What is this?
If you noticed that TakeLessons doesn't have an API or a way to export your own data you can use this package to get at it.

## How do I use it?

### Prerequisites

1. Install Chrome
2. Find the correct selenium driver version for your install [here](https://chromedriver.chromium.org/downloads)
3. Add it to PATH or make a note of where it is

### Example

```python
####
# Assume some db object you can save your data to
db = SomeDBStore()
####
from takelessons_scraper import session, Scraper
chromedriver_path = '/path/to/chromedriver'
username = 'username'
password = 'password'

with session(chromedriver_path) as tl_session:
    scraper = Scraper(tl_session)

    scraper.login(username, password)
    for chat in scraper.get_chat_history():
        db.save(chat) # ugly html string
```

## Notes:
Please consider this a hobby project to be used as reference. Since it is a scraper I expect it to fail as regularly as the source is updated... which could be at any time and not within my control.
