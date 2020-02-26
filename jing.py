import csv_generator as cg


def main():
    while True:
        print("Welcome to use world bank data collector. \n"
              "This version is only for African countries, more function will be update at the future.")

        country_name, country_code, country_income = cg.african_country_name()

        print("Next, you are going to use World Bank Database category to search for the data you need."
              "Download at https://github.com/srkucd/jing_s_data_collectior/blob/master/WDI_CETS.xls\n")

        world_indicators, world_data_country_code, column_header = cg.african_country_data()

        data_country_code, indicators = cg.data_cleaning(country_code, world_data_country_code, world_indicators)

        dataframe = cg.df_generator(country_code,
                                    country_name,
                                    country_income,
                                    data_country_code,
                                    indicators,
                                    column_header)

        final_dataframe = cg.one_more_column(dataframe)

        cg.csv_export(final_dataframe)
        print("Now, you can find your data in the project's directory.")

        restart = input('\nWould you like to restart? Enter (y)es or (n)o.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
