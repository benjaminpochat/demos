import xml.etree.ElementTree as ET
import os

'''
This script is a utility to convert data from https://www.data.gouv.fr/fr/datasets/service-public-fr-annuaire-de-l-administration-base-de-donnees-locales/
to a csv file that can be injected into Redis demos database.

To prepare the date :
1. Download and extract the file available at https://www.data.gouv.fr/fr/datasets/r/73302880-e4df-4d4c-8676-1a61bb997f3d
2. Create a folder "mairies"
3. Filter the files concerning the commune with a simple bash command : "mv organismes/*/mairie* ./mairies/"

Then you can run this script with the following command "python3 extract_communes_from_xml_open_data_file.py"
It will produce a csv file that can be used with the database initializing script "initialize_databse_fr_communes.py"
'''

os.remove('fr_communes.csv')
file_urls_fr_communes = open('fr_communes.csv', 'w')

for filename in os.listdir('mairies'):
    tree = ET.parse('mairies/' + filename)
    noms_commune = tree.findall(".//NomCommune")
    urls = tree.findall(".//Url")
    codes_insee = tree.findall(".//CodeInsee")
    nom_commune = ''
    url = ''
    if noms_commune.__len__() > 0 :
        nom_commune = noms_commune[0].text
    if urls.__len__() > 0 :
        url = urls[0].text.replace('http://', '').replace('https://', '')
    code_insee = tree.getroot().get('codeInsee')
    line = code_insee + ';' + nom_commune + ';' + url + '\r\n'
    file_urls_fr_communes.writelines([line])

file_urls_fr_communes.close()
