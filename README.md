# Instagram Automation Toolkit

Python/Selenium utilities for browser-based Instagram workflows, including checking follow relationships and sending reels to selected users.

## Features

- Headless Firefox automation with Selenium
- Environment-based credential configuration
- Command-line control for reel sharing
- Exported text reports for follow-status checks

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your credentials in `.env`:

```text
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

Never commit `.env` or passwords to source control.

## Usage

```bash
python send_reels.py --users username1 username2 --reels 3
python follow_check.py
```

Instagram's UI and automation behavior can change, so Selenium selectors may need maintenance as the site evolves.

## Tech Stack

**Python · Selenium · Firefox WebDriver · BeautifulSoup · CLI Automation**

## Resume Description

**Instagram Automation Toolkit | Python, Selenium**

Built browser-automation utilities with Selenium and headless Firefox to streamline repeatable Instagram workflows, added CLI-driven execution and environment-based credential handling, and separated browser setup, authentication, reporting, and workflow logic for maintainability.
