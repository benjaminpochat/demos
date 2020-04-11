insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (101, 'INSEE-57057', 48.9855,	6.37806, 'Béchy', 'FRANCE_COMMUNE', 'www.bechy.fr');
insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (102, 'INSEE-74138', 45.7881, 6.05507, 'Gruffy', 'FRANCE_COMMUNE', 'www.gruffy.fr');

insert into web_document (id, url, local_government_id) values ('dec9441d673a08fecbacb386a16553d8675a6765', 'https://www.bechy.fr/CR_2020_08_03.pdf', 101);
insert into web_document (id, url, local_government_id) values ('c63ad3727b9c6226e4f8e6434c11e6bacd439376', 'https://www.bechy.fr/CR_2020_09_03.pdf', 101);
insert into web_document (id, url, local_government_id) values ('1e1a996f769990b184e6c423d7d100caca212157', 'https://www.bechy.fr/CR_2020_10_03.pdf', 101);
insert into web_document (id, url, local_government_id) values ('ae90d604d6ca87e4d5a4c132b740ee2d8b35beac', 'https://www.bechy.fr/CR_2020_11_03.pdf', 101);
insert into web_document (id, url, local_government_id) values ('6ca4f8e2ed199a0150e9389c3b7e71547d1845a3',	'https://www.gruffy.fr/CR_2017_09_28.pdf', 102);
insert into web_document (id, url, local_government_id) values ('9a1831f9faab0e6499a9e6a1cd51ef65085aaad7',	'https://www.gruffy.fr/CR_2017_10_30.pdf', 102);
insert into web_document (id, url, local_government_id) values ('1d762a515a4bbc959938fa3dd5aa0c06adcf8fc3',	'https://www.gruffy.fr/CR_2017_12_04.pdf', 102);
