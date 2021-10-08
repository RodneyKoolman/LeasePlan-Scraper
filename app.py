import config, time, requests
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
scraper_follow_cars = True
scraper_check_every = 60
scraper_mail_from = config.your_from_mail
scraper_mail_to = config.your_to_mail
scraper_sendgrid_apikey = config.your_api_key
scraper_website_url = 'https://www.leaseplan.com/nl-nl/zakelijk-leasen/showroom/{}/?leaseOption[mileage]={}&leaseOption[contractDuration]={}&popularFilters=b3eb0313-9583-427d-9db2-782f29f83afb&fuelTypes={}&makemodel={}'.format(leaseplan_brand, leaseplan_mileage, leaseplan_duration, leaseplan_type, leaseplan_model)
scraper_last_run = 'never'
scraper_last_error = 'never'
scraper_run_count = 0
scraper_error_count = 0
scraper_mails_send = 0

def send_mail(current_car):
    global scraper_last_error, scraper_error_count, scraper_mails_send

    message = Mail(
    from_email=scraper_mail_from,
    to_emails=scraper_mail_to,
    subject='New {} available with id {}'.format(leaseplan_brand, current_car),
    html_content='New <strong>{}</strong> available with id <strong>{}</strong>.'.format(leaseplan_brand, current_car))

    try:
        sendgrid = SendGridAPIClient(scraper_sendgrid_apikey)
        sendgrid.send(message)
        scraper_mails_send += 1

    except Exception as e:
        scraper_last_error = datetime.now().strftime('%H:%M:%S')
        scraper_error_count += 1
        print('Error {}. Stopped parsing, retrying mail'.format(e))
        time.sleep(10)
        send_mail(current_car)

def main():
    global scraper_run_count, scraper_last_run, scraper_last_error, scraper_error_count

    while True:
        try:
            page = requests.get(scraper_website_url, timeout=10)
            parse = BeautifulSoup(page.content, 'html.parser')
            cars = parse.find_all('div', {'data-component':'VehicleCard'})

            for car in cars:
                current_car = car['data-key']
                if current_car not in scraper_processed_cars:
                    send_mail(current_car)
                    scraper_processed_cars.append(current_car)
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
    main()