# Demos

Demos is an experimentation for scraping city council reports from official city web sites, and archiving public deliberations in a centralized database.

The aim of this experimentation is to try how machine learning mecanisms can help to :
1. identify official city council reports through the web
2. archive these reports into one centralized database

If this experimentation is successful, this could offer some perspectives for indexing official local governments reports, and building a search engine for these data.

This project is the opportunity to use machine learning for civic tech.

## How it works ?

Demos is composed of 2 main modules :
* the training module
* the archiving module


## The training module

Before collecting and archiving the document, the algorithm has to be trained to recognize "official city council reports".
If you want to start archiving the report with the default algorithm, you can skip this paragraph and look directly to the "archiving module".

To train the algorithm, the following steps must be followed :

### Step 1 : collect some data from official city web sites

This steps consists in storing into the data base some content found in some official city web sites. 
The data collected will contain some "official report" and some other data. 

To run this step, use the following command :

```demos train collect```

This command collects all pdf documents found on official french "municipalités" web sites.

**/!\ WARNING : for this experimentation, only pdf files are considered, to limit the quantity of data analyzed. This is an important limitation.**

The process might be very long... You can make it shorter by limiting the number of web sites crawled. 
For instance to limit collecting the pdf files from 10 web sites :
 
 ```demos train collect -n 10```

More options for ```collect``` command are explained with the following comand :

 ```demos train collect -h```
 

### Step 2 : Classify manually the data collected to tell what is an "official report" and what is not

This steps consists in giving the algorithm some classified data to learn how recognize official reports from other data.

To run this step, use the following command :

```demos train classify```
 
This command iterates over the documents found on step 1. For each document :
* the text of the document is displayed
* the user is prompted to tell if the text is an "official report" or not

More options for ```clasify``` command are explained with the following command :

```demos train classify -h```


### Step 3 : Train the algorithm to recognize "official reports", based on data classified manually

This steps consists in training the algorithm (and build a model) with the data manually classified previously.

To run this step, use the following command :

```demos train model```

This command produces 2 files that can be used in the archiving module.


The algorithm is better trained as the quantity of data collected and manually classified is bigger.


## The archiving module

**/!\ WARNING : demos is an experimentation. A default trained algorithm is provided to try the process, but this default algorithm does not recognize all official city council reports. 
To build a better algorithm, follow the instructions to run the training module.**

To run this step, use the following command :

```demos archive```

This command browse all pdf documents found on official french "municipalités" web sites, 
and stores in the database only the ones that are recognized as official reports by the algorithm trained previously. 


## Technical aspects

### Technical requirements

#### Python 3.5 and dependencies

Demos run with python-3.5.

See [this documentation](https://docs.python.org/3/installing/index.html) to install python.

The python dependencies required are listed in the file :

```src/package/requirements.txt```

These dependencies can be installed with the following command :

```pip install --trusted-host pypi.python.org -r src/package/requirements.txt```
 

#### Redis database

To run both training and archiving modules, a Redis database must be run (tested with redis-5.0.2). 
To run Redis, please refer to [Redis documentation](https://redis.io/).

### Technical configuration

#### Main configuration

The main configuration file is ```src/main/resources/config.yml```

Please see the content of this file to know what can be configured.

The configuration values can be set in both manner :
* In the yml file directly
* In the command line with the following key value syntax ```demos <command> --<key> <value>```
    For instance, to set the redis database host in the command line for the archiving module :
    
    ```demo archive --database_host DBSERVER```
    
    Every keys of the yml file can be configured in command line.
    The configuration set in the command line are used in priority.  

#### Log configuration

Demos logs information during its process thanks to the logging python module. 
A logging configuration file can be found at this path :

```src/main/resources/logging.conf```

It can be customized, according to the [logging module documentation](https://docs.python.org/3/library/logging.config.html).  

### Run demos with docker

As demos is based on web scraping that might be long, it has been designed to be deployed numerously thanks to docker containers.
The idea is to run as many demos as possible in parallel, in many docker containers.

To run demos in a docker container :
[to be completed...]
