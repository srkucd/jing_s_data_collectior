import urllib.request
import json
import ssl
import pandas as pd

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
    return country_name_list, country_code_list, country_income_list


country_name, country_code, country_income = african_country_name()

def african_country_data():
    """
    This is just prototype, variable indicator and year will be input by user in our final version.
    It create two lists about indicator value, and ISO-2 code.
    :return: indicator value list,country code list.
    """
    while True:
        year = input("Please enter the year of data you need.")
        try:
            if (int(year) > 1959) and (int(year) < 2015):
                break
            else:
                print("The data only recorded from 1960 to 2014. please make sure your input is between 1960-2014.")
                continue
        except:
            print("Invalid value, please make sure you enter the number of the year(e.g., 1997).")
            continue

    while True:
        indicator = input("Please enter the indicator.")
        data_url = 'https://api.worldbank.org/v2/country/all/indicator/' + indicator + '?date=' + str(
        year) + '&per_page=999&format=json'
        try:
            the_world_data = json.loads(urllib.request.urlopen(data_url).read())[1]
            break
        except:
            print("Invalid indicator. Please use WDI_CETS.xls as the reference.")
            continue

    indicator_list = []
    country_code_list = []
    column_header = the_world_data[0].get('indicator').get('value')
    for each in the_world_data:
        if each.get('country').get('id') in country_code:
            indicator_list.append(each.get('value'))
            country_code_list.append(each.get('country').get('id'))
    return indicator_list, country_code_list, column_header


world_indicators, world_data_country_code, column_header = african_country_data()


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
            useful_position.append(changed_country_code.index(each))
    for each in useful_position:
        indicator_list.append(indicator[each])

    return country_code_list, indicator_list


data_country_code, indicators = data_cleaning(country_code, world_data_country_code, world_indicators)


def df_generator(target_country_code, country_name, country_income, data_country_code, indicator, header):
    """
    Combine the first indicator data and the country data as pandas dataframe.
    :param target_country_code: sorted country code
    :param country_name: country name sorted by target_country_code
    :param country_income: country income sorted by target_country_code
    :param data_country_code: unsorted country code, use as foreign key between two dataframe.
    :param indicator: indicator data sorted by data_country_income
    :param header: title of indicator data column.
    :return: Combined dataframe of the first indicator and country details.
    """
    df_country = pd.DataFrame(list(zip(target_country_code,country_name,country_income)),
                                   columns = ['Country Code','Country Name','Income Level'])

    df_data = pd.DataFrame(list(zip(data_country_code,indicator)),
                           columns = ['Country Code',str(header)])

    merged_df = df_country.merge(df_data, on='Country Code', how = 'inner')

    return merged_df

df = df_generator(country_code, country_name, country_income, data_country_code, indicators, column_header)
print(df.head())

