insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (101, 'INSEE-1', -4.09504985809, 48.4743003845, 'Béchy', 'FRANCE_COMMUNE', 'www.bechy.fr');

insert into scraping_session (id, creation, end_scraping, local_government_id) values (1, to_date('01-01-2020 07:00', 'DD-MM-YYYY HH24:MI'), to_date('01-01-2020 07:05', 'DD-MM-YYYY HH24:MI'), 101);
insert into scraping_session (id, creation, end_scraping, local_government_id) values (2, to_date('02-01-2020 03:01', 'DD-MM-YYYY HH24:MI'), to_date('02-01-2020 08:10', 'DD-MM-YYYY HH24:MI'), 101);
