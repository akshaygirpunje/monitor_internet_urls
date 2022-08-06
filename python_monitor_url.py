'''
This Python Web service monitors the provided urls & produces  metrics (on /metrics) 
and output a prometheus format when hitting the service http://webserverip/metrics url
'''
import prometheus_client as prom
import requests
import time
import json

'''
Variables
'''
RESPONSE_TIME_GAUGE = prom.Gauge('sample_external_url_response_ms', 'HTTP response in milliseconds', ["url"],multiprocess_mode='min')
STATUS_CODE_GAUGE = prom.Gauge('sample_external_url_up', 'Boolean status of site up or down', ["url"],multiprocess_mode='min')
URL_LIST = []


'''
Get the response time in ms for URL.
Return the response time in ms for URL.
'''
def get_response(url):
    response = requests.get(url)
    response_time = response.elapsed.total_seconds()
    print(url,'Response Time','--->',response_time)    
    return response_time

'''
Get the URL's HTTP status code like (200 / 503 / 400)  & 
set the status code value as 1 for 200 HTTP status code and value set to 0 for non 200 HTTP response code.
Return the status code as 1 or 0.
'''
def get_url_status(url):        
    response = requests.get(url)
    url_status_code=response.status_code
    if(url_status_code == 200):
        status_code=1
    else:
        status_code=0                       
    print(url,'Status Code','--->',status_code)
    return status_code
        
'''
Set the URL's Response code & status code recursively in Gauge.
'''
def set_values():
    try:
        while True:
            for url_name in URL_LIST:
                response_time = get_response(url_name)
                RESPONSE_TIME_GAUGE.labels(url=url_name).set(response_time)
                response_status = get_url_status(url_name)
                STATUS_CODE_GAUGE.labels(url=url_name).set(response_status)
                time.sleep(5)
    except TypeError:
        print('URLs list is empty,Please check the URLs in urls.json')
    except Exception:
        print('Please provide the valid URLs in urls.json or check the Network connectivity')

'''
Create the URLs list
-> Opening JSON file
-> Create the URLs list using returns JSON object dictionary
-> return URLs List
'''
def get_url_list():
    try:
        with open ('urls.json','r') as urls:
            data = json.load(urls)    
        for url in data:
            URL_LIST=data[url]
        return URL_LIST
    except IOError:
        print('File not found,Please check the file name')

'''
Main method
-> start the server on port 8001
-> Get the Urls list using get_url_list() function
-> Set the Response time & URL status code using set_values() function
'''
if __name__ == '__main__':
    try:
        prom.start_http_server(8001)
        URL_LIST=get_url_list()
        set_values()
    except OSError:
        print('8001 port Address is in use,please use diffrent port')
    except Exception:
        print('Please provide the valid URLs in urls.json or check the Network connectivity')
