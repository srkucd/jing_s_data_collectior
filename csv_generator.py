import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def african_country_name():
    """
    select all African countries name, income level and ISO-2-code.
    :return: country name list, country income list, country code list.
    """
    country_url = 'https://api.worldbank.org/v2/country/?per_page=999&format=json'
    the_world = json.loads(urllib.request.urlopen(country_url).read())[1]
    country_name_list = []
    country_income_list = []
    country_code_list = []
    middle_east_country_name = ['United Arab Emirates', 'Bahrain', 'Iran, Islamic Rep.', 'Iraq', 'Israel', 'Jordan',
                                'Kuwait',
                                'Lebanon', 'Malta', 'West Bank and Gaza', 'Qatar', 'Saudi Arabia', 'Sudan',
                                'Syrian Arab Republic',
                                'Yemen, Rep.']
    for each in the_world:
        if 'Africa' in each.get('region').get('value'):
            if each.get('name') not in middle_east_country_name:
                country_name_list.append(each.get('name'))
                country_income_list.append(each.get('incomeLevel').get('value'))
                country_code_list.append(each.get('iso2Code'))
            else:
                continue
        else:
            continue
    return country_name_list, country_income_list, country_code_list


country_name, country_income, country_code = african_country_name()


def african_country_data():
    """
    This is just prototype, variable indicator and year will be input by user in our final version.
    It create two lists about indicator value, and ISO-2 code.
    :return: indicator value list,country code list.
    """
    indicator = 'NY.GNP.ATLS.CD'
    year = 2014
    data_url = 'https://api.worldbank.org/v2/country/all/indicator/' + indicator + '?date=' + str(
        year) + '&per_page=999&format=json'
    the_world_data = json.loads(urllib.request.urlopen(data_url).read())[1]
    indicator_list = []
    country_code_list = []
    for each in the_world_data:
        indicator_list.append(each.get('value'))
        country_code_list.append(each.get('country').get('id'))
    return indicator_list, country_code_list


world_indicators, world_data_country_code = african_country_data()


def data_cleaning(standard_country_code, changed_country_code, indicator):
    """
    Erase useless data in list, in our prototype, only African data needed.
    :param standard_country_code: A group of countries list as the standard of data cleaning.
    :param changed_country_code: The country list needs to modify
    :param indicator: Data list about related indicator
    :return: cleaned country code list and indicator list, ready for CSV generation.
    """
    useful_position = []
    indicator_list = []
    country_code_list = []
    for each in changed_country_code:
        if each in standard_country_code:
            country_code_list.append(each)
            useful_position.append(country_code_list.index(each))
    for each in useful_position:
        indicator_list.append(indicator[each-1])
    
    return country_code_list, indicator_list

