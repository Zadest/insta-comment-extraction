# insta-comment-extraction
insta-comment-extraction is an application that allows you to scrape the texts of posts and their comments from a specified account from the current Instagram website (as of 31.05.2022). The software is merely an illustration of how scraping might work, please note that using it would violate Instagram's terms of use.

# Usage (please read the section above)
 - you need at least `python3.8` and the modules in `requirements.txt`
 - best practice is to create a virtual environment 
 ```bash
    python3.8 -m venv .env
    # activate .env
    (env) python -m pip install -r requirements.txt
 ```
 - Within the `.env/bin` you will need to place the executable [geckodriver](https://github.com/mozilla/geckodriver/releases) for your system
 - you also need to create a `config.py` containing:
```python
    USERNAME = "YOUR_USERNAME"
    PASSWORD = "YOUR_PASSWORD"
```
 - start the software with `python insta_cookies_login.py`
