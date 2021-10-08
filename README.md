# LeasePlan - Scraper

This app will let you scrape certain parts of LeasePlan and extract data of cars becoming available for lease.
Written and optimized for Azure Web Apps but can be used standalone as well.

- Scrapes certain url with modifiable filter
- Gets all current cars and adds them in-memory
- Send notification if a new car is available
- Ignores already processed cars
- Robust Exception-Handling
- **Note:** currently it uses a Dutch url-format which you need to change if you are from another country

**TODO**:
Follow car link and scrap details.

## Screenshot

![demo](/demo/demo.gif)

## Usage

This app uses SendGrid for mail notifications when cars become available. SendGrid can be used for free but you need to create an API key.
Make sure to change the config.your_from_mail, config.your_to_mail and config.your_api_key to reflect your SendGrid settings.

- **scraper_webservice_enabled** = True (enables dashboard and statistics)
- **scraper_mail_enabled** = True (enables mail notifications)

1. Adjust the script properties at the top
2. Setup and configure your environment (Python 3.8+)
3. Install the required modules in requirements.txt
4. Run app.py
6. Enjoy!

## Disclaimer

Use this app at your own risk. Do not flood sites with requests.

## Author

**Rodney Koolman**

Give a ⭐️ if you like this project!