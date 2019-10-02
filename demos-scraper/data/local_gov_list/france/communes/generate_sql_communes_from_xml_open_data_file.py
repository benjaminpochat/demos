if __name__ == '__main__':

    import xml.etree.ElementTree as ET
    import os
    import sys
    import re

    '''
    This script is a utility to convert data from https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/
    to a sql update script that can be run on a table including the communes, identified by their code insee.
    
    To prepare the date :
    1. Download and extract the file available at https://www.data.gouv.fr/fr/datasets/r/73302880-e4df-4d4c-8676-1a61bb997f3d
    2. Create a folder "mairies"
    3. Filter the files concerning the commune with a simple bash command : "mv organismes/*/mairie* ./mairies/"
    
    Then you can run this script with the following command "python3 generate_sql_communes_from_xml_open_data_file.py"
    '''

    mode = 'update'
    if sys.argv.__contains__('-i'):
        mode = 'insert'

    data_directory = '.'
    if sys.argv.__contains__('-d'):
        data_directory = sys.argv[sys.argv.index('-d') + 1]

    file_name = mode + '_fr_communes.sql'
    if os.path.exists(file_name):
        os.remove('update_fr_communes.sql')

    file_urls_fr_communes = open(file_name, 'w')


    for filename in os.listdir(data_directory):
        tree = ET.parse(data_directory + '/' + filename)
        noms_commune = tree.findall(".//NomCommune")
        urls = tree.findall(".//Url")
        latitudes = tree.findall(".//Latitude")
        longitudes = tree.findall(".//Longitude")
        codes_postaux = tree.findall(".//CodePostal")
        nom_commune = ''
        url = ''
        latitude = '0.0'
        longitude = '0.0'
        code_postal = ''
        if noms_commune.__len__() > 0:
            nom_commune = noms_commune[0].text.replace('\'', '\'\'')
            nom_commune = re.sub(r'^(.*)\sCedex(\s\d*)*$', r'\1', nom_commune)
        if urls.__len__() > 0 :
            url = urls[0].text.replace('http://', '').replace('https://', '')
        if latitudes.__len__() > 0 and latitudes[0].text != None:
            latitude = latitudes[0].text
        if longitudes.__len__() > 0 and longitudes[0].text != None:
            longitude = longitudes[0].text
        if codes_postaux.__len__() > 0 and codes_postaux[0].text != None:
            code_postal = codes_postaux[0].text
        code_insee = tree.getroot().get('codeInsee')
        if mode == 'insert':
            line = 'insert into local_government ' \
                    + '(id, codification, latitude, longitude, name, type, web_site, zip_code) ' \
                    + 'values (nextval(\'local_government_id_seq\'), \'' \
                    + code_insee + '\', ' \
                    + longitude + ', '\
                    + latitude + ', '\
                    + '\'' + nom_commune + '\', ' \
                    + '\'FRANCE_COMMUNE\', ' \
                    + '\'' + url + '\', '\
                    + '\'' + code_postal + '\'''); \r\n'
        else:
            line = 'update local_government set '\
                    + 'latitude = ' + latitude + ', '\
                    + 'longitude = ' + longitude + ', '\
                    + 'name = \'' + nom_commune + '\', '\
                    + 'type = \'FRANCE_COMMUNE\', '\
                    + 'web_site = \'' + url + '\', '\
                    + 'zip_code = \'' + code_postal + '\' '\
                    + 'where codification = \'' + code_insee + '\'; \r\n'
        file_urls_fr_communes.writelines([line])

    file_urls_fr_communes.close()
