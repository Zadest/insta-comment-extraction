# insta-comment-extraction
Repository for extracting insta comments for @ichbinsophiescholl

# Usage
 - you need at least `python3.8` and the modules in `requirements.txt`
 - best practice is to create a virtual environment 
 ```bash
    python3.8 -m venv .env
    # activate .env
    (env) python -m pip install -r requirements.txt
 ```
 - you also need to create a `config.py` containing:
```python
    USERNAME = "YOUR_USERNAME"
    PASSWORD = "YOUR_PASSWORD"
```
 - start the software with `python insta_cookies_login.py`