# 📷 Instagram Browser Automation — Archived

> **Status: Archived / Personal Learning Project**

## What is this project?

This repository contains experiments for **automating actions in a web browser on Instagram**.

Instead of manually performing every browser action, the Python program uses **Selenium** to open the website and interact with page elements.

The main purpose of the project was to learn how browser automation works.

## What can it do?

The repository contains experiments related to:

- Checking Instagram profiles.
- Checking whether accounts follow back.
- Sending reels through an automated browser workflow.
- Finding and interacting with webpage elements.

## How does browser automation work?

The basic idea is:

```text
Python program
      ↓
Open browser
      ↓
Open website
      ↓
Find a page element
      ↓
Click / read / interact
      ↓
Continue the workflow
```

Selenium acts as a bridge between the Python program and the web browser.

## Simple example

A person might manually do this:

```text
Open Instagram
     ↓
Open a profile
     ↓
Check information
     ↓
Perform an action
```

Browser automation attempts to make the computer perform those steps through code.

## Why is this repository archived?

A browser automation project depends on the website it controls.

If Instagram changes its page structure, button names, login flow or anti-automation behaviour, the script may stop working even when the Python code has not changed.

The platform can also change its authentication systems, protections and terms of service.

Because of this, this repository is kept as a **learning experiment** rather than a main portfolio project.

## Security

Never put passwords, session information, API keys or other secrets directly in source code.

Use environment variables for local experiments and follow the platform's current rules and terms.

## Main technologies

- **Python** — application and automation logic
- **Selenium** — controls a real web browser from code
- **Environment variables** — keep sensitive configuration outside source code
- **Pytest** — tests selected parts of the code

## Project structure

```text
follow_check.py              → Follow-back checking experiment
follow_back/                 → Follow-back automation code
send_reels.py                → Reel-sending experiment
tests/                       → Automated tests
.env.example                → Example configuration file
requirements.txt             → Python dependencies
```

## Technical terms explained

**Browser automation** — Using a program to perform actions in a web browser that a person would normally perform manually.

**Selenium** — A tool that allows Python and other programming languages to control web browsers, such as opening pages, finding elements and interacting with them.

**Web element / page element** — A part of a webpage that the browser represents separately, such as a button, text field, link or image.

**DOM (Document Object Model)** — The structure a browser creates from a webpage's HTML. Programs such as Selenium can use this structure to find and interact with elements.

**HTML** — The markup language used to describe the structure and content of webpages.

**Selector** — A way of telling Selenium which webpage element to find, for example by using an element's attributes, class or text.

**Environment variable** — A value stored outside the source code and provided to the application when it runs. It is commonly used for configuration and secrets.

**Session information** — Information that can keep a user logged in to a website. It should be treated as sensitive data.

**Automation workflow** — A sequence of automated actions performed in a particular order.

**Pytest** — A Python testing framework used to write and run automated tests.

## What does this project demonstrate?

This project demonstrates the basic workflow behind browser automation:

**Python → browser control → webpage elements → automated actions → testing**

It demonstrates **Python, Selenium, browser automation, DOM interaction, environment-based configuration and testing**.

## Portfolio recommendation

This repository should not be one of the first projects shown to recruiters. It is retained as a personal learning experiment.

The stronger portfolio projects are:

1. **Flight-Alert-System** — flight-price monitoring, MySQL, analytics and automation
2. **RAG-Sytem** — document AI and semantic search
3. **Fourier-Image-Drawing** — mathematics, image processing and visualisation
4. **Seq2Seq-Model** — machine translation and deep learning
5. **sudoku** — algorithms and problem solving
6. **LRU-Cache** — data structures and performance
