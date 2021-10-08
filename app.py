import settings, time, requests
from flask import *
from threading import Thread
from datetime import datetime
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

leaseplan_brand = 'tesla'
leaseplan_mileage = 10000
leaseplan_duration = 60
leaseplan_type = 'volledig%20elektrisch'
leaseplan_model = 'model-3'
scraper_processed_cars = []
scraper_follow_cars = False
scraper_check_every = 60
scraper_mail_from = settings.your_from_mail
scraper_mail_to = settings.your_to_mail
scraper_sendgrid_apikey = settings.your_api_key
scraper_webservice_host = '0.0.0.0'
scraper_webservice_port = 80
scraper_domain = 'https://www.leaseplan.com'
scraper_start_url = 'https://www.leaseplan.com/nl-nl/zakelijk-leasen/showroom/{}/?leaseOption[mileage]={}&leaseOption[contractDuration]={}&popularFilters=b3eb0313-9583-427d-9db2-782f29f83afb&fuelTypes={}&makemodel={}'.format(leaseplan_brand, leaseplan_mileage, leaseplan_duration, leaseplan_type, leaseplan_model)
scraper_last_run = 'never'
scraper_last_error = 'never'
scraper_last_new_car = 'none'
scraper_last_new_link = 'none'
scraper_run_count = 0
scraper_error_count = 0
scraper_mails_send = 0
scraper_webserver = Flask(__name__)

def webserver_start():
     scraper_webserver.run(host=scraper_webservice_host, port=scraper_webservice_port, debug=False, use_reloader=False)

@scraper_webserver.route('/')
def webserver_content():
    return '<h1>LeasePlan Scraper</h1> </br></br><b>Status:</b></br> Scraper last run: {}</br> Scraper last error: {}</br></br>Scraper run counter: {}</br>Scraper error counter: {}</br></br>Scraper processed cars: {}</br>Scraper mails send: {}</br></br>Scraper is currently looking for <b>{} {}</b> with <b>{}</b> km and a duration of <b>{}</b>.</br></br>Last new car: {}</br>{}</br></br>Scraper checks every: {} seconds</br>Scraper curring time: {}'.format(scraper_last_run, scraper_last_error, scraper_run_count, scraper_error_count, scraper_processed_cars, scraper_mails_send, leaseplan_brand, leaseplan_model, leaseplan_mileage, leaseplan_duration, scraper_last_new_car, scraper_last_new_link, scraper_check_every, datetime.now())
    
def send_mail(current_car, current_car_link):
    global scraper_last_error, scraper_error_count, scraper_mails_send

    message = Mail(
    from_email=scraper_mail_from,
    to_emails=scraper_mail_to,
    subject='New {} available with id {}'.format(leaseplan_brand, current_car),
    html_content='New <strong>{}</strong> available with id <strong>{}</strong>. {}'.format(leaseplan_brand, current_car, current_car_link))

    try:
        sendgrid = SendGridAPIClient(scraper_sendgrid_apikey)
        sendgrid.send(message)
        scraper_mails_send += 1

    except Exception as e:
        scraper_last_error = datetime.now().strftime('%H:%M:%S')
        scraper_error_count += 1
        print('Error {}. Stopped parsing, retrying mail'.format(e))
        time.sleep(10)
        send_mail(current_car, current_car_link)

def parse(page):
    page = requests.get(page, timeout=5)
    parsed_page = BeautifulSoup(page.content, 'html.parser')

    return parsed_page

def main():
    global scraper_run_count, scraper_last_run, scraper_last_error, scraper_error_count

    while True:
        try:
            parsed_page = parse(scraper_start_url)
            cars = parsed_page.find_all('div', {'data-component':'VehicleCard'})

            for car in cars:
                current_car = car['data-key']
                current_car_link = car.find("a")['data-e2e-id']

                if current_car not in scraper_processed_cars:                    
                    #Experimental - Not functional yet, set scraper_follow_cars to false
                    if(scraper_follow_cars):
                        page = parse(scraper_domain + current_car_link)
                        specifications = page.find_all('div', {'data-component':'Specification'})
                        print(specifications)

                    
                    send_mail(current_car, current_car_link)
                    scraper_processed_cars.append(current_car)
                    scraper_last_new_car = current_car
                    scraper_last_new_link = current_car_link
                    time.sleep(5)

            scraper_run_count += 1
            scraper_last_run = datetime.now().strftime('%H:%M:%S')

            print('Done parsing. Processed cars are {}'.format(scraper_processed_cars))

        except Exception as e:
            scraper_error_count += 1
            scraper_last_error = datetime.now().strftime('%H:%M:%S')
            
            print('Error {}. Stopped parsing, retrying loop'.format(e))
            time.sleep(10)
            pass

        print('Waiting {} seconds for next parse'.format(scraper_check_every))
        time.sleep(scraper_check_every)

if __name__ == "__main__":
    try:
        Thread(target=webserver_start).start()
        main()
    except Exception as e:
        print('Unexpected error {}. Application cannot start.'.format(e))