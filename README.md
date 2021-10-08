# LeasePlan - Scraper

This app will let you continuously scrape certain parts of LeasePlan and extract data of cars becoming available for lease.
It has a webservice where you can check the status of the scraper, it can also notify you via mail when a car is available.

- Scrapes certain url with modifiable filter
- Gets all current cars and adds them in-memory
- Send notification if a new car is available
- Ignores already processed cars
- Robust Exception-Handling
- **Note:** currently it uses a Dutch url-format which you need to change if you are from another country

**TODO**:
- Follow car link and scrap car details
- Style the dashboard webservice

## Demo

![demo](/demo/demo.gif)

## Usage

This app uses SendGrid for mail notifications when cars become available. SendGrid can be used for free but you need to create an API key.
Make sure to change the config.your_from_mail, config.your_to_mail and config.your_api_key to reflect your SendGrid settings.

- **scraper_webservice_enabled** = True (enables dashboard and statistics)
- **scraper_mail_enabled** = True (enables mail notifications)

1. Adjust the script properties at the top
2. Setup and configure your environment (Python 3.8+)
3. Install the required modules in requirements.txt (pip3 install -r requirements.txt)
4. Run app.py (Tip: if you are using a standalone server, use PM2 to manage running python scripts)
6. Enjoy!

## Disclaimer

Use this app at your own risk. Do not flood sites with requests.

## Author

**Rodney Koolman**

Give a ⭐️ if you like this project!