# delib-archiver

An experimentation for scraping city council reports from official city web sites, and archiving public deliberations in a structured manner.

The aim of these experimentation is to facilitate access to local government decisions through the web.


## How it (should) works ?

The target mecanism of this program is to run regularly a process based on the following steps :
1. crawling and scraping the content of official city web sites
2. among this bunch of data, identifiyng the content that is new official city council reports
3. extracting structured data from council reports such as dates, seperate deliberations, topics, etc...
4. storing this stuctured data, and publishing it on the internet

To acheive this goal, several technical challenges must be resolved.
The following paragraphs explain how to dive in them.


## Crawling official city web sites

[... to be completed]


## Identifying official city council reports among a bunch of data

To realize this recognition, we use Tensor Flow machine learning framework.
To learn Tensor Flow how to recognize a spécific type of document, you have to train the machine with a set of data which is already classified.
Today, we are still on the way gathering such a dataset and training the machine.
To do so, we use documents that are published as pdf files in official city web sites :
- it represents a smaller quantity of data than the whole content of web sites
- a lot of city web sites (among french ones) publish their council reports as pdf files.

To train the TensorFlow model, we have to :
- gather pdf files from web sites (see the paragraphe above). 
- convert pdf files into text files : from the root dir of the project, run "./scripts/convert_pdf_to_files.sh"
- classify them into 2 catégories : "city_council_reports" and "others" : [... to be completed]
- train the model : [... to be completed]


## Extracting structured data from reports

[... nothing done so far]


## Store and publish

[... nothing done so far]
