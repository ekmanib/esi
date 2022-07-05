import os
import pandas as pd
import numpy as np
import glob
import csv

# Reading support files for the inclusion of geolocation data
isoc = pd.read_csv('../esi/files_support/ISOcodesEs.csv', sep = '\t', usecols=['País', 'iso2'])
countries = pd.read_csv('../esi/files_support/worldcountries.csv', sep = '\t', usecols=['country', 'latitude', 'longitude'])
cities = pd.read_csv('../esi/files_support/worldcities.csv', usecols=['city', 'lat', 'lng', 'country'])
cities_codes = pd.read_csv('../esi/files_support/cantones_codes.csv')

# In cities, filter to country == Ecuador as there are ecuadorian cities that share names with other cities abroad
# Inmidiately after, drop the column country as it will otherwise generate problem down the line
cities = cities.loc[cities['country'] == 'Ecuador']
cities.drop(columns=['country'], inplace=True)

# Series.str.title method capitalizes each word in a string
cities_codes['CANTON'] = cities_codes['CANTON'].str.title()

# iso codes dictionary in spanish

# All dictionaries

movi_dict = {
    'Entrada': 1,
    'Salida' : 2
}

naci_dict = {
    'Ecuatoriano' : 1,
    'Extranjero'  : 2
}

sex_dict = {
    'Hombre': 1,
    'Mujer' : 2,
}

tran_dict = {
    'Vía terrestre' : 1, 
    'Vía Maritimo'  : 2, 
    'Vía Aérea'     : 3, 
    'Vía fluvial'   : 4
}

mot_dict = {
    'Residencia' : 1, 
    'Turismo'    : 2, 
    'Otros'      : 3, 
    'Eventos'    : 4, 
    'Negocios'   : 5,
    'Estudios'   : 6
}

mes_dict = {
    'Abril':4, 
    'Agosto':8, 
    'Diciembre':12, 
    'Enero':1, 
    'Febrero':2, 
    'Julio':7,
    'Junio':6, 
    'Marzo':3, 
    'Mayo':5, 
    'Noviembre':11, 
    'Octubre':10, 
    'Septiembre':9
}

cntn_dict = {
    'Huaquillas' : 707, 
    'Guayaquil' : 901, 
    'Manta' : 1308, 
    'Salinas' : 2403, 
    'Tulcán' : 401, 
    'Quito' : 1701,
    'Esmeraldas' : 801, 
    'Latacunga' : 501, 
    'San Lorenzo' : 805, 
    'Santa Cruz' : 2003, 
    'Machala' : 701,
    'San Cristóbal' : 2001, 
    'Cuenca' : 101, 
    'Sucumbíos' : 2105, 
    'Isabela' : 2002, 
    'Macará' : 1108
}

iso_esp = {
    'Afganistán': 'AF', 'Albania': 'AL', 'Alemania': 'DE', 'Andorra': 'AD', 'Angola': 'AO', 'Anguila': 'AI', 
    'Antártida': 'AQ', 'Antigua y Barbuda': 'AG', 'Arabia Saudita': 'SA', 'Argelia': 'DZ', 'Argentina': 'AR', 
    'Armenia': 'AM', 'Aruba': 'AW', 'Australia': 'AU', 'Austria': 'AT', 'Azerbaiyán': 'AZ', 'Bahamas': 'BS', 
    'Bahrein': 'BH', 'Bailía de Guernsey': 'GG', 'Bangladesh': 'BD', 'Barbados': 'BB', 'Belarús': 'BY', 'Bélgica': 'BE', 
    'Belice': 'BZ', 'Benín': 'BJ', 'Bermudas': 'BM', 'Bolivia': 'BO', '`Bosnia y Hercegovina`': 'BA', 'Botsuana': 'BW', 
    'Brasil': 'BR', 'Brunéi': 'BN', 'Bulgaria': 'BG', 'Burkina Faso': 'BF', 'Burundi': 'BI', 'Bután': 'BT', 'Cabo Verde': 'CV', 
    'Cambodia': 'KH', 'Camerún': 'CM', 'Canadá': 'CA', 'Catar': 'QA', 'Chad': 'TD', 'Chequia': 'CZ', 'Chile': 'CL', 'China': 'CN', 
    'Chipre': 'CY', 'Ciudad del Vaticano': 'VA', 'Colombia': 'CO', 'Comores': 'KM', 'Congo': 'CG', 'Corea del Norte': 'KP', 
    'Corea del Sur': 'KR', 'Costa de Marfil': 'CI', 'Costa Rica': 'CR', 'Croacia': 'HR', 'Cuba': 'CU', 'Curaçao': 'CW', 
    'Dinamarca': 'DK', 'Dominica': 'DM', 'Ecuador': 'EC', 'Egipto': 'EG', 'El Salvador': 'SV', 'Emiratos Árabes Unidos': 'AE', 
    'Eritrea': 'ER', 'Eslovaquia': 'SK', 'Eslovenia': 'SI', 'España': 'ES', 'Estados Federados de Micronesia': 'FM', 'Estados Unidos': 'US', 
    'Estonia': 'EE', 'Esuatini': 'SZ', 'Etiopía': 'ET', 'Fiji': 'FJ', 'Filipinas': 'PH', 'Finlandia': 'FI', 'Francia': 'FR', 
    'Gabón': 'GA', 'Gambia': 'GM', 'Georgia': 'GE', 'Georgia del Sur y las Islas Sandwich del Sur': 'GS', 'Ghana': 'GH', 
    'Gibraltar': 'GI', 'Granada': 'GD', 'Grecia': 'GR', 'Groenlandia': 'GL', 'Guadalupe': 'GP', 'Guam': 'GU', 'Guatemala': 'GT', 
    'Guayana': 'GY', 'Guayana Francesa': 'GF', 'Guinea': 'GN', 'Guinea Ecuatorial': 'GQ', 'Guinea-Bissau': 'GW', 'Haití': 'HT', 
    'Honduras': 'HN', 'Hong Kong': 'HK', 'Hungría': 'HU', 'India': 'IN', 'Indonesia': 'ID', 'Irán': 'IR', 'Iraq': 'IQ', 'Irlanda': 'IE', 
    'Isla Bouvet': 'BV', 'Isla de Man': 'IM', 'Isla de Navidad': 'CX', 'Isla de San Martín': 'MF', 'Isla Mauricio': 'MU', 
    'Isla Norfolk': 'NF', 'Islandia': 'IS', 'Islas Åland': 'AX', 'Islas Caimán': 'KY', 'Islas Cocos': 'CC', 'Islas Cook': 'CK', 
    'Islas Feroe': 'FO', 'Islas Heard y McDonald': 'HM', 'Islas Malvinas': 'FK', 'Islas Marianas del Norte': 'MP', 'Islas Marshall': 'MH', 
    'Islas Pitcairn': 'PN', 'Islas Salomón': 'SB', 'Islas Turcas y Caicos': 'TC', 'Islas Vírgenes (UK)': 'VG', 'Islas Vírgenes Americanas': 'VI', 
    'Israel': 'IL', 'Italia': 'IT', 'Jamaica': 'JM', 'Japón': 'JP', 'Jersey': 'JE', 'Jordania': 'JO', 'Kazajstán': 'KZ', 'Kenia': 'KE', 'Kirguistán': 'KG', 
    'Kiribati': 'KI', 'Kosovo': 'XK', 'Kuwait': 'KW', 'Laos': 'LA', 'Lesotho': 'LS', 'Letonia': 'LV', 'Líbano': 'LB', 'Liberia': 'LR', 
    'Libia': 'LY', 'Liechtenstein': 'LI', 'Lituania': 'LT', 'Luxemburgo': 'LU', 'Macao': 'MO', 'Macedonia del Norte': 'MK', 
    'Madagascar': 'MG', 'Malasia': 'MY', 'Malaui': 'MW', 'Maldivas': 'MV', 'Malí': 'ML', 'Malta': 'MT', 'Marruecos': 'MA', 
    'Martinica': 'MQ', 'Mauritania': 'MR', 'Mayotte': 'YT', 'México': 'MX', 'Moldavia': 'MD', 'Mongolia': 'MN', 'Montenegro': 'ME', 
    'Montserrat': 'MS', 'Mozambique': 'MZ', 'Myanmar': 'MM', 'Namibia': 'NA', 'Nauru': 'NR', 'Nepal': 'NP', 'Nicaragua': 'NI', 
    'Níger': 'NE', 'Nigeria': 'NG', 'Niue': 'NU', 'Noruega': 'NO', 'Nueva Caledonia': 'NC', 'Nueva Zelandia': 'NZ', 'Omán': 'OM', 
    'Países Bajos': 'NL', 'Pakistán': 'PK', 'Palaos': 'PW', 'Palestina': 'PS', 'Panamá': 'PA', 'Papúa Nueva Guinea': 'PG', 
    'Paraguay': 'PY', 'Perú': 'PE', 'Polinesia Francesa': 'PF', 'Polonia': 'PL', 'Portugal': 'PT', 'Principado de Mónaco': 'MC', 
    'Puerto Rico': 'PR', 'Reino Unido': 'GB', 'República Centroafricana': 'CF', 'República Democrática del Congo': 'CD', 
    'República Dominicana': 'DO', 'Reunión': 'RE', 'Ruanda': 'RW', 'Rumania': 'RO', 'Rusia': 'RU', 'Sáhara Occidental': 'EH', 
    'Samoa': 'WS', 'Samoa Americana': 'AS', 'San Bartolomé': 'BL', 'San Cristóbal y Nieves': 'KN', 'San Marino': 'SM', 
    'San Pedro y Miquelón': 'PM', 'San Vicente y las Granadinas': 'VC', 'Santa Elena, Ascensión y Tristán de Acuña': 'SH', 
    'Santa Lucía': 'LC', 'Santo Tomé y Príncipe': 'ST', 'Senegal': 'SN', 'Serbia': 'RS', 'Seychelles': 'SC', 'Sierra Leona': 'SL', 
    'Singapur': 'SG', 'Sint Maarten': 'SX', 'Siria': 'SY', 'Somalia': 'SO', 'Sri Lanka': 'LK', 'Sudáfrica': 'ZA', 'Sudán': 'SD', 
    'Sudán del Sur': 'SS', 'Suecia': 'SE', 'Suiza': 'CH', 'Surinam': 'SR', 'Svalbard y Jan Mayen': 'SJ', 'Tailandia': 'TH', 
    'Taiwán': 'TW', 'Tanzania': 'TZ', 'Tayikistán': 'TJ', 'Territorio Británico del Océano Índico': 'IO', 
    'Territorios Australes y Antárticos Franceses': 'TF', 'Timor Oriental': 'TL', 'Togo': 'TG', 'Tokelau': 'TK', 'Tonga': 'TO', 
    'Trinidad y Tobago': 'TT', 'Túnez': 'TN', 'Turkmenistán': 'TM', 'Turquía': 'TR', 'Tuvalu': 'TV', 'Ucrania': 'UA', 'Uganda': 'UG', 
    'Uruguay': 'UY', 'Uzbekistán': 'UZ', 'Vanuatu': 'VU', 'Venezuela': 'VE', 'Vietnam': 'VN', 'Wallis y Futuna': 'WF', 'Yemen': 'YE', 
    'Yibuti': 'DJ', 'Zambia': 'ZM', 'Zimbabue': 'ZW'
}

# variables to be selected as they are of interest and are present in all dataframes, as noted from basic exploration in nb
varnames = [
    'tip_movi', 'tip_naci', 'anio_movi', 'mes_movi',
    'dia_movi', 'sex_migr', 'nac_migr', 'via_tran', 
    'mot_viam', 'pais_prod', 'lug_prod', 'pais_res',
    'jef_migr', 'can_jefm', 
    # 'edad' >> May include but it needs transformations to categorical, probably by ranges of age
]

def process(file_path):
    # function read in a csv file, transforms it and then writes a new one in another folder
    
    # some files use ';' as separator whereas others use ','. Open the file beforehand and determine which delimiter to use
    with open(file_path, errors="ignore") as f:
        reader = csv.reader(f)
        line = next(reader)
        if len(line) == 1:
            delim = ';'

        else:
            delim = ','

    # read in data file and also get its name
    df = pd.read_csv(file_path, usecols = varnames, sep = delim, nrows=10000)
    file_name = file_path.split('\\')[-1]

    # strip all whitespace in all columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    # replace values of 'mes_movie' column through dictionary items
    df.replace({'mes_movi':mes_dict}, inplace=True)

    # rename certain fields to get year, month and day columns
    df.rename(columns={'anio_movi':'year', 'mes_movi':'month', 'dia_movi':'day'}, inplace=True)

    # use year, month and day columns to create a single date column / collapse them into `date`
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    # drop unnecessary data that is now compacted in the date variable
    df.drop(['year', 'month', 'day'], axis=1, inplace=True)

    # Create a dictionary with new names for the countries that weren't matched 
    countries_dict = {
        'Antigua República Yugoslava de Macedonia': 'Macedonia del Norte',
        'Barein' : 'Bahrein',
        'Bielorrusia' : 'Belarús',
        'Bonaire, San Eustaquio y Saba' : 'Not',
        'Bosnia y Herzegovina' : '`Bosnia y Hercegovina`',
        'Brunei Darussalam' : 'Brunéi',
        'Camboya' : 'Cambodia',
        'Comoras' : 'Comores',
        'Curazao' : 'Curaçao',
        'Estados Unidos de América' : 'Estados Unidos',
        'Federación de Rusia' : 'Rusia',
        'Fiyi' : 'Fiji',
        'Guernsey' : 'Not',
        'Guinea-Bisau' : 'Guinea-Bissau',
        'Guyana' : 'Guayana',
        'Hong Kong (Región Administrativa Especial de China)' : 'Hong Kong',
        'Irak' : 'Iraq',
        'Isla de Navidad (Chistmas)' : 'Isla de Navidad',
        'Islas Aland' : 'Islas Åland',
        'Islas Georgias del Sur y Sándwich  del Sur' : 'Georgia del Sur y las Islas Sandwich del Sur',
        'Islas Heard y Mc Donald' : 'Islas Heard y McDonald',
        'Islas Malvinas (Falkland)' : 'Islas Malvinas',
        'Islas Marianas Septentrionales' : 'Islas Marianas del Norte',
        'Islas Norfolk' : 'Isla Norfolk',
        'Islas Ultramarinas de EE UU' : 'Not',
        'Islas Vírgenes Británicas' : 'Islas Vírgenes (UK)',
        'Islas Vírgenes de los Estados Unidos' : 'Islas Vírgenes Americanas',
        'Kazajistán' : 'Kazajstán',
        'Lesoto' : 'Lesotho',
        'Mauricio' : 'Isla Mauricio',
        'Micronesia (Estados Federados de)' : 'Estados Federados de Micronesia',
        'Mónaco' : 'Principado de Mónaco',
        'Nueva Zelanda' : 'Nueva Zelandia',
        'Pitcairn' : 'Islas Pitcairn',
        'Polinesia francesa' : 'Polinesia Francesa',
        'República Checa' : 'Chequia',
        'República Democrática Popular Lao' : 'Laos',
        'República Popular Democrática de Corea' : 'Corea del Norte',
        'República de Corea del Sur' : 'Corea del Sur',
        'República de Moldovia' : 'Moldavia',
        'República Árabe Siria' : 'Siria',
        'San Martín' : 'Sint Maarten',
        'San Martín (Parte francesa)' : 'Isla de San Martín',
        'Santa Sede (Vaticano)' : 'Ciudad del Vaticano',
        'Sint Maarten (Parte Holandesa)' : 'Sint Maarten',
        'Suazilandia' : 'Esuatini',
        'Taiwán (República de China)' : 'Taiwán',
        'Tanzania (República Unida de)' : 'Tanzania',
        'Tanzania (República Unida de) ' : 'Tanzania',
        'Timor-Leste' : 'Timor Oriental',
        'Islas Cocos ó Keeling' : 'Islas Cocos',
        'Islas Wallis y Futuna' : 'Wallis y Futuna'
    }

    # create dictionary to change can_jefm column in df
    cantones_dict = {
        'Tulcan' : 'Tulcán',
        'Macara' : 'Macará',
        'Sucumbios' : 'Nueva Loja',
        'Sucumbíos' : 'Nueva Loja',
        'San Lorenzo' : 'San Lorenzo de Esmeraldas',
        'Espindola' : 'Loja',
        'Espíndola' : 'Loja', 
        'Chinchipe' : 'Zamora', 
        'Zapotillo' : 'Loja',
        'Puerto el Carmen del Putumayo' : 'Nueva Loja', 
        'Aguarico': 'Puerto Francisco de Orellana',
        'San Cristóbal' : 'Puerto Baquerizo Moreno', 
        'Isabela' : 'Puerto Villamil', 
        'Lago Agrio':'Nueva Loja',
    }

    # use dictionaries to replace columns' values.
    # Important to get merge df with
    df.replace({
        'pais_prod': countries_dict,
        'pais_res' : countries_dict,
        'nac_migr' : countries_dict,
        'can_jefm' : cantones_dict
    }, inplace=True)

    # important merging step
    # first merge now includes lat and lng coordinates for Ecuadorian cities
    # second merge includes iso codes for countries on the column `nac_migr`, then, with iso codes, lat and lng are included
    # forth merge includes iso codes for countries on the columns `pais_prod`, then, with iso codes, lat and lng are included
    df0 = pd.merge(df, cities, how = 'left', left_on='can_jefm', right_on='city')
    df1 = pd.merge(df0, isoc, how = 'left', left_on = 'nac_migr', right_on = 'País')
    df2 = pd.merge(df1, countries, how = 'left', left_on = 'iso2', right_on = 'country')
    df3 = pd.merge(df2, isoc, how = 'left', left_on = 'pais_prod', right_on = 'País', suffixes=('', '_pais_prod'))
    df4 = pd.merge(df3, countries, how = 'left', left_on = 'iso2_pais_prod', right_on = 'country',suffixes=('', '_pais_prod'))
    
    # return to df after droping unimportant and repetitive columns
    df = df4.drop(['city', 'iso2', 'iso2_pais_prod', 'País', 'País_pais_prod'], axis=1)

    df['iso_pais_res'] = df['pais_res']

    # define dictionary with new names for variables
    refactor_dict = {
        'lat'                : 'lat_can_jefm',
        'lng'                : 'lng_can_jefm',
        'country'            : 'iso_nac_migr',
        'latitude'           : 'lat_nac_migr',
        'longitude'          : 'lng_nac_migr',
        'country_pais_prod'  : 'iso_pais_prod',
        'latitude_pais_prod' : 'lat_pais_prod',
        'longitude_pais_prod': 'lng_pais_prod',
    }

    # rename using refactor_dict
    df.rename(columns = refactor_dict, inplace=True)

    # in spite of the loss of information, remove observations whenever `pais_prod` is set to 'Not'
    # df.drop(df[df['pais_prod'] == 'Not'].index, inplace=True)

    # In order to ensure consistency, I must set to NaNs lng and lat whenever iso codes are NaNs
    df.loc[df['pais_prod'] == "Not", ['lat_pais_prod', 'lng_pais_prod']] = np.NaN
    df.loc[df['pais_prod'] == "Not", ['lat_pais_prod', 'lng_pais_prod']] = np.NaN

    # aggregate all variable, as they are all relevant, to monthly frequency
    df = df.groupby(
        [df['date'].dt.strftime('%Y-%m'),
        'tip_movi', 'tip_naci', 'sex_migr', 'nac_migr', 'via_tran',
        'mot_viam', 'pais_prod', 'lug_prod', 'pais_res', 'iso_pais_res', 'jef_migr', 'can_jefm',
        'lat_can_jefm', 'lng_can_jefm', 'iso_nac_migr', 'lat_nac_migr',
        'lng_nac_migr', 'iso_pais_prod', 'lat_pais_prod', 'lng_pais_prod']
    ).size().reset_index().rename(columns={0:'count'})

    # replace columns' values with respective dictionaries
    df.replace({
        'iso_pais_res': iso_esp,
        'tip_movi' : movi_dict,
        'tip_naci' : naci_dict,
        'sex_migr' : sex_dict,
        'via_tran' : tran_dict,
        'mot_viam' : mot_dict,
        'can_jefm' : cntn_dict
    }, inplace=True)

    # set new datetime column as index
    df.set_index('date', inplace=True)

    df.to_csv(f'../esi/files/{file_name}',sep = ',', encoding = 'utf-8-sig')


if __name__ == '__main__':
    file_paths = glob.glob(os.path.join('../esi/downloads/', 'esi*.csv'))
    for fpath in file_paths:
        process(fpath)
