const Apify = require('apify');
const Kafka = require('kafka-node')

Apify.main(async () => {
    // Apify.openRequestQueue() is a factory to get a preconfigured RequestQueue instance.
    // We add our first request to it - the initial page the crawler will visit.
    const requestQueue = await Apify.openRequestQueue();

    await requestQueue.addRequest({ url: 'https://metz.fr' });

    const kafkaClient = new Kafka.KafkaClient({kafkaHost: 'localhost:9092' });
    const kafkaProducer = new Kafka.Producer(kafkaClient);

    // handlePage is called for each page reached by the crawler
    const handlePage = async ({ request, page }) => {
        
        console.log(`Processing ${request.url}...`);
        
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
        await registerPdfUrls(pdfUrls, kafkaProducer);
        
        // Find a link to the next page and enqueue it if it exists.
        const infos = await Apify.utils.enqueueLinks({
            page,
            requestQueue,
            selector: 'a',
            pseudoUrls: ['https://metz.fr/[.*]', 'https://www.metz.fr/[.*]', 'http://metz.fr/[.*]', 'http://www.metz.fr/[.*]']
        });
        
        if (infos.length === 0)
            console.log(`${request.url} is the last page!`);
    };

    const handleErrorRequest = async ({ request }) => {
        console.log(`Request ${request.url} failed too many times`);
        await Apify.pushData({
            '#debug': Apify.utils.createRequestDebugInfo(request),
        });
    };

    const crawler = new Apify.PuppeteerCrawler({
        requestQueue,
        launchPuppeteerOptions: {
            headless: true
        },
        handlePageFunction: handlePage,

        // This function is called if the page processing failed more than maxRequestRetries+1 times.
        handleFailedRequestFunction: handleErrorRequest,
    });

    // Run the crawler and wait for it to finish.
    await crawler.run();

    console.log('Crawler finished.');
});

async function registerPdfUrls(pdfUrls, kafkaProducer) {
    //await Apify.pushData(data);
    pdfUrls.forEach(pdfUrl => {
        var payloads = [
            {
                topic: 'UnclassifiedPdfUrl',
                messages: pdfUrl
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
