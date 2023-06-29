# Goodreads to Amazon Wishlist Automation

This repository contains a Python script that automates the process of transferring books from your Goodreads "to-read" list to an Amazon Wishlist. It parses through your Goodreads list, finds each book on Amazon and then adds it to your specified Amazon Wishlist.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Python
* You have a Goodreads "to-read" list ID. You can find it in the address goodreads.com/review/list/ > 167212401 < ?ref=nav_mybooks
* You have an Amazon account
* You have your Amazon login credentials

## Installation

To install the dependencies, follow these steps:

* Clone the repository:

    ```
    git clone https://github.com/janis-sijanovs/goodreads-to-amazon-wishlist.git
    cd goodreads-to-amazon-wishlist
    ```

* Install the Python dependencies from the `requirements.txt` file:

    ```
    pip install -r requirements.txt
    ```

## Configuration

To use this script, you must set several configuration variables in the `.env` file. Follow these steps:

* Rename `.env.example` to `.env`

    ```
    mv .env.example .env
    ```

* Open the `.env` file and fill in your personal information for the required variables (Goodreads and Amazon credentials etc.). Be sure to save the file.

## Usage

To use the script, navigate to the repository folder and run the script:

```bash
python main.py
