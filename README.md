# Rappi Restaurant Web Scraper

Extract prices and descriptions of restaurants in Rappi

This Python script uses Selenium, Pygsheets, Numpy and Pandas to scrape the menu items and prices of selected restaurants from the Rappi website. The results are stored in a Google Sheet using Pygsheets.

## Requirements

To run this script, you will need:

- Python 3
- The following Python libraries: `selenium`, `numpy`, `pandas`, and `pygsheets`
- The `webdriver_manager` library
- The ChromeDriver executable, which can be installed with `webdriver_manager`

## Usage

1. Clone this repository to your local machine.
2. Install the necessary Python libraries listed above.
3. Install ChromeDriver using `webdriver_manager`.
4. Set up a Google Sheet and obtain the credentials file. Follow the instructions at [Pygsheets Quickstart](https://pygsheets.readthedocs.io/en/stable/authorizing.html) to authorize Pygsheets.
5. Modify the `resturants` and `links` lists to include the desired restaurants and their corresponding links.
6. Run the script using Python 3.

## License

This project is licensed under the MIT License. See `LICENSE` for more information.
