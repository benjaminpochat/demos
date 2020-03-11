const Apify = require('apify');
const Kafka = require('kafka-node');
const Utils = require('./utils.js');
const fetch = require('node-fetch');

const demosCoreHost = 'localhost';
const demosCorePort = '8080';
const demosCoreUrl = 'http://' + demosCoreHost + ':' + demosCorePort;
const demosKafkaHost = 'localhost';
const demosKafkaPort = '9092';

Apify.main(async () => {

    const scrapingSession = await getScrapingSession();
    const localGovernment = scrapingSession.localGovernment;
    const localGovernementStartUrl = Utils.getUrlWithProtocol(localGovernment.webSite);
    const domainName = Utils.getDomainNameFromLocalGovernment(localGovernment);

    console.log(`Starting scraping session #${scrapingSession.id} for ${localGovernementStartUrl}...`);

    // Apify.openRequestQueue() is a factory to get a preconfigured RequestQueue instance.
    // We add our first request to it - the initial page the crawler will visit.
    const requestQueue = await Apify.openRequestQueue();

    await requestQueue.addRequest({ url: localGovernementStartUrl });

    // handlePage is called for each page reached by the crawler
    const handlePageFunction = getHandlePageFunction(scrapingSession, requestQueue, domainName);

    // This function is called if the page processing failed more than maxRequestRetries+1 times.
    const handleFailedRequestFunction = getHandleErrorRequestFunction();

    const crawler = new Apify.PuppeteerCrawler({
        requestQueue,
        maxConcurrency: 10,
        maxRequestsPerCrawl: 1000,
        launchPuppeteerOptions: {
            headless: true
        },
        handlePageFunction: handlePageFunction,
        handleFailedRequestFunction: handleFailedRequestFunction,
    });

    // Run the crawler and wait for it to finish.
    await crawler.run();
    await updateScrapingSession(scrapingSession);
    console.log(`Crawler finished scraping session #${scrapingSession.id}.`);
});

function getHandlePageFunction(scrapingSession, requestQueue, domainName) {
    let localGovernment = scrapingSession.localGovernment
    return async ({ request, page }) => {
        // A function to be evaluated by Puppeteer within the browser context.
        const collectLinksToPdf = linksToPdf => {
            const pdfUrls = [];
            // We're getting all links to pdf files present in the page
            linksToPdf.forEach(linkToPdf => {
                pdfUrls.push(linkToPdf.href);
            });
            return pdfUrls;
        };
        const pdfUrls = await page.$$eval('a[href$=\'.pdf\']', collectLinksToPdf);
        // Store the results to the default dataset.
        await registerPdfUrls(pdfUrls, localGovernment);
        // Find a link to the next page and enqueue it if it exists.
        const infos = await Apify.utils.enqueueLinks({
            page,
            requestQueue,
            selector: 'a',
            pseudoUrls: ['https://' + domainName + '/[.*]',
            'https://www.' + domainName + '/[.*]',
            'http://' + domainName + '/[.*]',
            'http://www.' + domainName + '/[.*]']
        });
        if (infos.length === 0)
            console.log(`${request.url} is the last page!`);
    };
}

function getHandleErrorRequestFunction() {
    return async ({ request }) => {
        console.log(`Request ${request.url} failed too many times`);
        await Apify.pushData({
            '#debug': Apify.utils.createRequestDebugInfo(request),
        });
    };
}

async function registerPdfUrls(pdfUrls, localGovernment) {
    const kafkaProducer = getKafkaProducer();

    pdfUrls.forEach(pdfUrl => {
        let pdfUrlAgregate = {
            url: pdfUrl,
            localGovernment: localGovernment
        }
        var payloads = [
            {
                topic: 'UnclassifiedPdfUrl',
                messages: JSON.stringify(pdfUrlAgregate),
                timestamp: Date.now()
            }
        ]
        kafkaProducer.send(payloads, function(message){
            console.log('Url ' + pdfUrl + ' sent to kafka.');
            if (message) {
                console.log(message);
            }
        })
    });
}

function getKafkaProducer() {
    const kafkaClient = new Kafka.KafkaClient({ kafkaHost: demosKafkaHost + ':' + demosKafkaPort });
    const kafkaProducer = new Kafka.Producer(kafkaClient);
    return kafkaProducer;
}

async function getScrapingSession() {
    const response = await fetch(
        demosCoreUrl + '/scrapingSessions',
        {method: 'GET'});
    const scrapingSession = await response.json(); 
    return scrapingSession;
}

async function updateScrapingSession(scrapingSession) {
    scrapingSession.endScraping = (new Date()).toISOString();
    await fetch(demosCoreUrl + '/scrapingSessions', {
        method: 'PUT',
        body: JSON.stringify(scrapingSession),
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
    });
}
