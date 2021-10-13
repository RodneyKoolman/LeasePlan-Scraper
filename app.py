import time, requests
from flask import *
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# LeasePlan settings
# Note: LeasePlan sometimes seems to ignore deeper filters
leaseplan_search_brand = 'tesla'
leaseplan_search_model = 'model-3'
leaseplan_search_filters = 'b3eb0313-9583-427d-9db2-782f29f83afb'
leaseplan_contract_mileage = 10000
leaseplan_contract_duration = 60

# Scraper settings
scraper_processed_vehicles = []
scraper_webservice_enabled = True
scraper_webservice_host = '0.0.0.0'
scraper_webservice_port = 80
scraper_mail_enabled = True
scraper_check_every = 60
scraper_follow_vehicles = False # Experimental
scraper_sendgrid_apikey = '[change_this]'
scraper_sendgrid_from = '[change_this]'
scraper_sendgrid_to = '[change_this]'
scraper_base_domain = 'https://www.leaseplan.com'
scraper_start_url = f'{scraper_base_domain}/nl-nl/zakelijk-leasen/showroom/{leaseplan_search_brand}/?leaseOption[mileage]={leaseplan_contract_mileage}&leaseOption[contractDuration]={leaseplan_contract_duration}&popularFilters={leaseplan_search_filters}&makemodel={leaseplan_search_model}'
scraper_last_run_time = '00:00:00'
scraper_last_error_time = '00:00:00'
scraper_last_error_message = 'none'
scraper_last_vehicle = 'none'
scraper_last_vehiclelink = 'none'
scraper_total_run_count = 0
scraper_total_error_count = 0
scraper_total_mails_sent = 0
scraper_first_run = True
scraper_webserver = Flask(__name__)

def webserver_start():
    scraper_webserver.run(host=scraper_webservice_host, port=scraper_webservice_port, debug=False, use_reloader=False)

@scraper_webserver.route('/')
def index():
    return render_template('index.html', lastrun=scraper_last_run_time, lasterror=scraper_last_error_time, runcounter=scraper_total_run_count, errorcounter=scraper_total_error_count, vehiclesinmemory=len(scraper_processed_vehicles) , lastaddedvehicle=scraper_last_vehicle, mailssent=scraper_total_mails_sent, checkevery=scraper_check_every, servertime=datetime.now().strftime('%H:%M:%S'), lastaddedvehiclelink=scraper_last_vehiclelink, vehiclebrand=leaseplan_search_brand, vehiclemodel=leaseplan_search_model, vehicleduration=leaseplan_contract_duration, vehiclemileage=leaseplan_contract_mileage, mailenabled=scraper_mail_enabled, firstrun=scraper_first_run, errormessage=scraper_last_error_message)

def parse(page):
    page = requests.get(page, timeout=5)
    return BeautifulSoup(page.content, 'html.parser')

def error(ex):
    global scraper_last_error_time, scraper_last_error_message, scraper_total_error_count

    scraper_last_error_time = datetime.now().strftime('%H:%M:%S')
    scraper_last_error_message = ex
    scraper_total_error_count += 1
    print(f'Error {scraper_last_error_message}. Retrying soon')
    time.sleep(5)

def mail(current_vehicle, current_vehiclelink):
    global scraper_total_mails_sent

    message = Mail(
    from_email = scraper_sendgrid_from,
    to_emails = scraper_sendgrid_to,
    subject = f'New {leaseplan_search_brand} available with id {current_vehicle}',
    html_content = f'New <strong>{leaseplan_search_brand}</strong> available with id <a href={scraper_base_domain+current_vehiclelink}><strong>{current_vehicle}</strong></a>.')

    try:
        sendgrid = SendGridAPIClient(scraper_sendgrid_apikey)
        sendgrid.send(message)
        scraper_total_mails_sent += 1

    except Exception as ex:
        error(ex)
        mail(current_vehicle, current_vehiclelink)

def main():
    global scraper_total_run_count, scraper_last_run_time, scraper_last_vehicle, scraper_last_vehiclelink, scraper_first_run

    while True:
        try:
            parsed_page = parse(scraper_start_url)
            vehicles = parsed_page.find_all('div', {'data-component':'VehicleCard'})

            for vehicle in vehicles:
                current_vehicle = vehicle['data-key']
                current_vehiclelink = vehicle.find("a")['data-e2e-id']

                if current_vehicle not in scraper_processed_vehicles:                    
                    
                    #Experimental - Not functional yet, set scraper_follow_vehicles to false
                    if(scraper_follow_vehicles):
                        page = parse(scraper_base_domain + current_vehiclelink)
                        specifications = page.find_all('div', {'data-component':'Specification'})
                        print(specifications)

                    if(scraper_mail_enabled and not scraper_first_run):
                        mail(current_vehicle, current_vehiclelink)

                    scraper_processed_vehicles.append(current_vehicle)
                    scraper_last_vehicle = current_vehicle
                    scraper_last_vehiclelink = scraper_base_domain+current_vehiclelink
                    time.sleep(2)

            scraper_first_run = False
            scraper_total_run_count += 1
            scraper_last_run_time = datetime.now().strftime('%H:%M:%S')

            print(f'Done scraping. Processed vehicles are {scraper_processed_vehicles}')

        except Exception as ex:
            error(ex)

        print(f'Waiting {scraper_check_every} seconds for next scrape')
        time.sleep(scraper_check_every)

if __name__ == "__main__":
    try:
        if(scraper_webservice_enabled):
            Thread(target=webserver_start).start()
        main()
    except Exception as ex:
        print(f'Unexpected error {ex}. Application cannot start.')