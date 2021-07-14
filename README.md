# Scrape the chat logs from TakeLessons

## What is this?
If you're irritated that TakeLessons doesn't have an API or a way to export logs you can use this package to get at it.

## Who is this for?
If you have a TakeLessons account and want to get your own data out in an automated way. 

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
chromdriver_path = '/path/to/chromedriver'
username = 'username'
password = 'password'

with session(chromedriver_path) as tl_session:
    scraper = Scraper(tl_session)

    scraper.login(username, password)
    for chat in scraper.get_chat_history():
        db.save(chat) # ugly html string
```


