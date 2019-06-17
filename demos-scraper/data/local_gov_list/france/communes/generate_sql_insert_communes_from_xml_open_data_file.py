if __name__ == '__main__':

    import xml.etree.ElementTree as ET
    import os

    '''
    This script is a utility to convert data from https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/
    to a sql file that can be injected into a relational demos database.
    
    To prepare the date :
    1. Download and extract the file available at https://www.data.gouv.fr/fr/datasets/r/73302880-e4df-4d4c-8676-1a61bb997f3d
    2. Create a folder "mairies"
    3. Filter the files concerning the commune with a simple bash command : "mv organismes/*/mairie* ./mairies/"
    
    Then you can run this script with the following command "python3 generate_sql_insert_communes_from_xml_open_data_file.py"
    '''
    #os.remove('fr_communes.sql')
    file_urls_fr_communes = open('fr_communes.sql', 'w')
    mairies_dir_path = '/home/benjamin/Bureau/all_20190619/mairies'

    for filename in os.listdir(mairies_dir_path):
        tree = ET.parse(mairies_dir_path + '/' + filename)
        noms_commune = tree.findall(".//NomCommune")
        urls = tree.findall(".//Url")
        latitudes = tree.findall(".//Latitude")
        longitudes = tree.findall(".//Longitude")
        nom_commune = ''
        url = ''
        latitude = '0.0'
        longitude = '0.0'
        if noms_commune.__len__() > 0:
            nom_commune = noms_commune[0].text.replace('\'', '\'\'')
        if urls.__len__() > 0 :
            url = urls[0].text.replace('http://', '').replace('https://', '')
        if latitudes.__len__() > 0 and latitudes[0].text != None:
            latitude = latitudes[0].text
        if longitudes.__len__() > 0 and longitudes[0].text != None:
            longitude = longitudes[0].text
        code_insee = tree.getroot().get('codeInsee')
        line = 'insert into local_government (id, codification, latitude, longitude, name, type, web_site) values (nextval(\'local_government_id_seq\'), \'' \
               + code_insee + '\', ' \
               + longitude + ', '\
               + latitude + ', '\
               + '\'' + nom_commune + '\', ' \
               + '\'FRANCE_COMMUNE\', ' \
               + '\'' + url + '\'); \r\n'
        file_urls_fr_communes.writelines([line])

    file_urls_fr_communes.close()
