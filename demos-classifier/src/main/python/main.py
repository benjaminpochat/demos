import requests
import json
from kafka import KafkaConsumer

from commons.configuration import Configuration
from process.rest_client_pdf_classifier import RestClientPdfClassifier


def _save_official_council_report(web_document):
    print("Saving WebDocument with url " + web_document['url'])
    url = _get_rest_service_url()
    content = _get_rest_service_content(web_document)
    print('Sending POST request :')
    print('- url : ' + url)
    print('- content : ' + json.dumps(content))
    _call_rest_service(url=url, data=content)


def _get_rest_service_url():
    demos_core_host = Configuration().get_demos_core_host()
    demos_core_port = Configuration().get_demos_core_port()
    url = 'http://' + demos_core_host + ':' + demos_core_port + '/webDocuments'
    return url


def _get_rest_service_content(web_document):
    return {
        'url': web_document['url'],
        'localGovernment':
            {'id': web_document['localGovernment']['id']},
        'id': web_document['id']}


def _call_rest_service(url: str, data: dict):
    response = requests.post(url=url,
                             json=data,
                             headers={
                                 'Accept': 'application/json, text/plain, */*',
                                 'Content-Type': 'application/json;charset=utf-8'
                             })
    if response.status_code != 200:
        print('POST ' + url + ' status : {}'.format(response.status_code))
    else:
        print('POST ' + url + ' status : {}'.format(response.status_code))
    return response


consumer = KafkaConsumer('UnclassifiedPdfContent', bootstrap_servers='localhost:9092', group_id='classifier')
classifier = RestClientPdfClassifier()
for consumer_record in consumer:
    unclassified_web_document = json.loads(consumer_record.value)
    classification = classifier.classify(unclassified_web_document['textContent'])
    if classification.isOfficialCouncilReport():
        print('The PDF at ' + unclassified_web_document['url'] + ' has been classified as an official city council report')
        _save_official_council_report(unclassified_web_document)
    else:
        print('The PDF at ' + unclassified_web_document['url'] + ' has not been classified as an official city council report')
