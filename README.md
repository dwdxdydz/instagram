# 📷 Instagram Browser Automation — Archived

> **Status: Archived / Personal Learning Project**

## What is this project?

This project contains experiments for **automating actions in a web browser on Instagram**.

Instead of manually performing every browser action, the program uses Selenium to open the website and interact with page elements.

The project was mainly created to learn how browser automation works.

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
Open Instagram
      ↓
Find a page element
      ↓
Click / read / interact
      ↓
Continue the workflow
```

Selenium acts like a program-controlled browser.

## Why is this repository archived?

Instagram's website can change its page structure and element names. When that happens, an automation script that depends on the old structure can stop working.

The platform can also change its login systems, anti-automation protections and policies.

Because of this, this repository is kept as a **learning experiment** rather than a main portfolio project.

## Security

Never put passwords, session information, API keys or other secrets directly in the source code.

Use environment variables for local experiments and always follow the platform's current rules and terms.

## Main technologies

- **Python** — automation logic
- **Selenium** — controls the web browser
- **Environment variables** — keep credentials outside the code
- **Pytest** — tests selected helper logic

## What I learned

This project helped demonstrate:

- Browser automation
- Finding webpage elements
- Automating multi-step workflows
- Working with environment variables
- Writing tests

## Portfolio recommendation

This is not one of the projects I would highlight first when applying for jobs.

The stronger portfolio projects are:

1. **Flight-Alert-System** — flight-price monitoring, MySQL, analytics and automation
2. **RAG-Sytem** — document AI and semantic search
3. **Fourier-Image-Drawing** — mathematics, image processing and visualization
4. **Seq2Seq-Model** — machine translation and deep learning
5. **sudoku** — algorithms and problem solving
6. **LRU-Cache** — data structures and performance
