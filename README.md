# LeasePlan - Scraper

This app will let you continuously scrape certain parts of LeasePlan and extract data of vehicles becoming available for lease.
It has a webservice where you can check the status of the scraper and it can also notify you via mail when a vehicle is available.

- Scrapes certain url with modifiable filter
- Gets all current vehicles and adds them in-memory
- Sends notification if a new vehicle is available
- Ignores already processed vehicles
- Robust Exception-Handling
- Web dashboard with statistics
- Mail notifications are disabled on first run (change scraper_first_run to False if you don't want this behavior)
- **Note:** currently it uses a Dutch url-format which you need to change if you are from another country

**TODO**:
- ~~Style the dashboard webservice~~
- Follow vehicle link and scrape vehicle details
- Remove hardcoded dutch url parts
- Support https/certificate for Flask

## Demo

![demo](/demo/demo-scraper.gif)

## Usage

This app uses SendGrid for mail notifications when vehicles become available. SendGrid can be used for free but you need to create an API key.
Make sure to change the scraper_sendgrid_apikey, scraper_sendgrid_from and scraper_sendgrid_to to reflect your SendGrid settings.

**Note:** LeasePlan sometimes seems to ignore deeper filters  
**Note:** If you make filters empty '', they are ignored  

**The best method is to go to leaseplan.com, search for vehicles with the desired filters. Look at the url and paste those values in the appy.py settings section.**

leaseplan_search_brand = 'tesla' -> Set this to any vehicle brand  
leaseplan_search_model = 'model-3' -> Set this to any vehicle model  
leaseplan_search_filters = 'b3eb0313-9583-427d-9db2-782f29f83afb' -> Set this to any leaseplan filter  
leaseplan_search_textfilter = 'Model 3' -> If leaseplan_search_model doesn't work, use this  
leaseplan_contract_mileage = 10000 -> Set this to any contract mileage  
leaseplan_contract_duration = 60 -> Set this to any contract duration  

scraper_first_run = True -> Edit this only if you want mail notifications to be send on first run  
scraper_webservice_enabled = True -> Enable or disable the webservice  
scraper_webservice_host = '0.0.0.0' -> Change the host address  
scraper_webservice_port = 80 -> Change the host port  
scraper_mail_enabled = True -> Enable or disable mail notifications 
scraper_parse_timeout = 5 -> Set the timeout in seconds the scraper should try to parse a webpage
scraper_check_pause = 60 -> Set the interval in seconds at which the scraper is checking leaseplan  
scraper_error_pause = 5 -> Set the interval in seconds at which the scraper pauses during an error
scraper_add_pause = 2 -> Set the interval in seconds at which the scraper pauses after adding a vehicle
scraper_follow_vehicles = False -> Experimental, do not use this yet  
scraper_sendgrid_apikey = '[change_this]' -> Sendgrid settings for mail notifications  
scraper_sendgrid_from = '[change_this]' -> Sendgrid settings for mail notifications  
scraper_sendgrid_to = '[change_this]' -> Sendgrid settings for mail notifications  
scraper_base_domain = 'https://www.leaseplan.com' -> Domain url, edit only if you know what you are doing  
scraper_start_url = f'{scraper_base_domain}/nl-nl/zakelijk-leasen/showroom/{leaseplan_search_brand}/?leaseOption[mileage]={leaseplan_contract_mileage}&leaseOption[contractDuration]={leaseplan_contract_duration}&popularFilters={leaseplan_search_filters}&makemodel={leaseplan_search_model}' -> Start search url, edit only if you know what you are doing  
scraper_last_run_time = '00:00:00' -> Do not edit this  
scraper_last_error_time = '00:00:00' -> Do not edit this  
scraper_last_error_message = 'none' -> Do not edit this  
scraper_last_vehicle = 'none' -> Do not edit this  
scraper_last_vehiclelink = 'none' -> Do not edit this  
scraper_total_run_count = 0 -> Do not edit this  
scraper_total_error_count = 0 -> Do not edit this  
scraper_total_mails_sent = 0 -> Do not edit this  
scraper_processed_vehicles = [] -> Do not edit this  
scraper_webserver = Flask(__name__) -> Do not edit this  

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