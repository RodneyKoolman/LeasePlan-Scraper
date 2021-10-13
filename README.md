# LeasePlan - Scraper

This app will let you continuously scrape certain parts of LeasePlan and extract data of cars becoming available for lease.
It has a webservice where you can check the status of the scraper and it can also notify you via mail when a car is available.

- Scrapes certain url with modifiable filter
- Gets all current cars and adds them in-memory
- Sends notification if a new car is available
- Ignores already processed cars
- Robust Exception-Handling
- Web dashboard with statistics
- Mail notifications are disabled on first run (change scraper_first_run to False if you don't want this behavior)
- **Note:** currently it uses a Dutch url-format which you need to change if you are from another country

**TODO**:
- ~~Style the dashboard webservice~~
- Follow car link and scrape car details
- Remove hardcoded dutch url parts
- Support https/certificate for Flask

## Demo

![demo](/demo/demo.gif)

## Usage

This app uses SendGrid for mail notifications when cars become available. SendGrid can be used for free but you need to create an API key.
Make sure to change the settings.your_from_mail, settings.your_to_mail and settings.your_api_key to reflect your SendGrid settings.

**LeasePlan filter settings**  
**Note:** LeasePlan sometimes seems to ignore deeper filters  
**Note:** If you make filters empty '', they are ignored  
The best method is to go to leaseplan.com, search for a vehicle with the desired filters. Look at the url and paste those values in the settings.

- leaseplan_search_brand = 'tesla' -> Set this to any vehicle brand
- leaseplan_search_model = 'model-3' -> Set this to any vehicle model
- leaseplan_search_filters = 'b3eb0313-9583-427d-9db2-782f29f83afb' -> Set this to any filter
- leaseplan_search_textfilter = 'Model 3' -> If leaseplan_search_model doesn't work, use this
- leaseplan_contract_mileage = 10000 -> Set this to any vehicle model you want to scrape
- leaseplan_contract_duration = 60

- **scraper_webservice_enabled** = True (enables dashboard and statistics)
- **scraper_mail_enabled** = True (enables mail notifications)

1. Adjust the script properties at the top
2. Setup and configure your environment (Python 3.6+ required)
3. Install the required modules in requirements.txt (pip3 install -r requirements.txt)
4. Run app.py (Tip: if you are using a standalone server, use PM2 to manage running python scripts)
6. Enjoy!

## Disclaimer

Use this app at your own risk. Do not flood sites with requests.

## Author

**Rodney Koolman**

Give a ⭐️ if you like this project!