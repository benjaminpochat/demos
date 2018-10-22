#!/usr/bin/env bash

# CC Sud Messin
scrapy crawl pdf_spider -a start_url="http://www.sudmessin.fr/accueil/documents-a-telecharger/cr-conseils-communautaires/" -a allowed_domain="sudmessin.fr"

# Sallanches
scrapy crawl pdf_spider -a start_url="http://www.sallanches.fr/2-hotel-de-ville.htm" -a allowed_domain="sallanches.fr"

# Avranches
scrapy crawl pdf_spider -a start_url="http://www.avranches.fr/Mairie/Vie-municipale" -a allowed_domain="avranches.fr"
scrapy crawl pdf_spider -a start_url="http://www.avranches.fr/Mairie/Vie-municipale/Conseil-Municipal" -a allowed_domain="avranches.fr"

# Port Vendres
scrapy crawl pdf_spider -a start_url="https://port-vendres.com/vie-municipale" -a allowed_domain="port-vendres.com"

# Guérande
scrapy crawl pdf_spider -a start_url="http://www.ville-guerande.fr/votre-mairie/le-conseil-municipal" -a allowed_domain="ville-guerande.fr"

# Bagneres de Bigorre
scrapy crawl pdf_spider -a start_url="http://www.ville-bagneresdebigorre.fr/publications-categories" -a allowed_domain="ville-bagneresdebigorre.fr"

# Valence
scrapy crawl pdf_spider -a start_url="http://www.valence.fr/fr/connaitre-la-mairie/la-vie-municipale/le-conseil-municipal.html" -a allowed_domain="valence.fr"


