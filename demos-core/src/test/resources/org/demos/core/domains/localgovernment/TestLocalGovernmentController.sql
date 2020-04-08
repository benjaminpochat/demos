insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (101, 'INSEE-1', -4.09504985809, 48.4743003845, 'Béchy', 'FRANCE_COMMUNE', 'www.bechy.fr');
insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (102, 'INSEE-2', 1, 1, 'Béthune', 'FRANCE_COMMUNE', 'www.bethune.fr');
insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (103, 'INSEE-3', 1, 2, 'Pornic', 'FRANCE_COMMUNE', 'www.pornic.fr');

insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (201, 'SIREN-2', -4.09504985809, 48.4743003845, 'CC Sud Messin', 'FRANCE_INTERCOMMUNALITE', 'www.sudmessin.fr');

insert into local_government_overlapping_local_governments (local_government_id, overlapping_local_governments_id, overlapping_local_governments_key) values (101, 201, 'FRANCE_INTERCOMMUNALITE');

insert into web_document (id, url, local_government_id) values (301, 'http://doc1.pdf', 101);
insert into web_document (id, url, local_government_id) values (302, 'http://doc2.pdf', 101);
insert into web_document (id, url, local_government_id) values (303, 'http://doc3.pdf', 102);
insert into web_document (id, url, local_government_id) values (304, 'http://doc4.pdf', 103);
insert into web_document (id, url, local_government_id) values (305, 'http://doc5.pdf', 201);
