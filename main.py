import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    """
    Main method, allows user to choose which part of the project to run.
    """
    user_input = input("Which part of the project would you like to run?\nEnter A, B, C or exit: ")
    if user_input == "A":
        cat_data()
    elif user_input == "B":
        num_data()
    elif user_input == "C":
        time_ser_data()
    elif user_input == "exit":
        quit()
    else:
        print("Incorrect entry, please try again.")
        main()


def cat_data():
    """
    Displays two bar charts to compare four categories of housing and their prices in two regions of the UK.
    """

    df = pd.read_csv("A_housePriceData_2021/Average-prices-Property-Type-2021-05_wrangled.csv")

    i = 0
    london_df = pd.DataFrame()
    newcastle_df = pd.DataFrame()
    # Separates the data by region and does not add unnecessary rows
    while i < len(df):
        if df.iloc[i]["Region_Name"] == "London":
            london_df = pd.concat([pd.DataFrame({"propertyType": [df.iloc[i]["propertyType"]],
                                                 "averagePrice": [df.iloc[i]["averagePrice"]]}),
                                   london_df], ignore_index=True)
            i += 1
        else:
            newcastle_df = pd.concat([pd.DataFrame({"propertyType": [df.iloc[i]["propertyType"]],
                                                    "averagePrice": [df.iloc[i]["averagePrice"]]}),
                                      newcastle_df], ignore_index=True)
            i += 1

    london_average_prices = pd.DataFrame()
    newcastle_average_prices = pd.DataFrame()
    # Separates region data into house types
    for dataframe in [london_df, newcastle_df]:
        # Both Semi_Detached and Detached contain "Detached" so requires manipulation to get the right data
        detached_and_semi_detached = dataframe[dataframe["propertyType"].str.contains("Detached")]
        semi_detached = dataframe[dataframe["propertyType"].str.contains("Semi_Detached")]
        # Remove values from detached_and_semi_detached that exist in semi_detached
        detached = pd.merge(detached_and_semi_detached, semi_detached, how='outer', indicator=True)
        detached = detached.loc[detached["_merge"] == "left_only"].drop("_merge", axis=1)
        terraced = dataframe[dataframe["propertyType"].str.contains("Terraced")]
        flat = dataframe[dataframe["propertyType"].str.contains("Flat")]

        # Calculates average for all house types
        # /1000 to make y-axis values smaller on the graph
        average_data = pd.DataFrame({"Detached": [detached["averagePrice"].mean() / 1000],
                                     "Semi_Detached": [semi_detached["averagePrice"].mean() / 1000],
                                     "Terraced": [terraced["averagePrice"].mean() / 1000],
                                     "Flat": [flat["averagePrice"].mean() / 1000]})

        # If london_average_prices is unpopulated then populate
        if len(london_average_prices) == 0:
            london_average_prices = average_data

        # If newcastle_average_prices is unpopulated then populate
        elif len(newcastle_average_prices) == 0:
            newcastle_average_prices = average_data

    # Configuration settings to make plots clearer and more informative
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.tight_layout(w_pad=2)
    fig.suptitle("Comparison of four categories of housing and their prices in two\nregions of the UK")
    plt.subplots_adjust(top=0.85, bottom=0.1, left=0.1)
    columns = ["Detached", "Semi-\nDetached", "Terraced", "Flat"]

    # First bar chart for London data
    ax1.bar(columns, list(london_average_prices.iloc[0]), color="blue")
    ax1.set_title("London", color="blue")
    ax1.set_ylabel("Average price in thousands (£)")
    ax1.set_ylim(0, 700)
    ax1.yaxis.grid()

    # Second bar chart for Newcastle data
    ax2.bar(columns, list(newcastle_average_prices.iloc[0]), color="orange")
    ax2.set_title("Newcastle", color="orange")
    ax2.set_ylabel("Average price in thousands (£)")
    ax2.set_ylim(0, 700)
    ax2.yaxis.grid()
    plt.show()

    main()


def num_data():
    """
    Displays a scatter graph comparing the relationship between broadband upload and download speeds in all regions of
    the UK. Calculates the correlation coefficient, regression line and outliers and displays these on the graph.
    """

    df = pd.read_csv("B_broadbandData_2021/202006_fixed_laua_performance_wrangled.csv")

    # Finds all average download values not in the IQR and shows which are outliers in down_outliers
    down_q1 = df["averageDown"].quantile(0.25)
    down_q3 = df["averageDown"].quantile(0.75)
    down_iqr = down_q3 - down_q1
    down_lower_lim = down_q1 - 1.5 * down_iqr
    down_upper_lim = down_q3 + 1.5 * down_iqr
    down_outliers = (df["averageDown"] < down_lower_lim) + (df["averageDown"] > down_upper_lim)

    # Finds all average upload values not in the IQR and shows which are outliers in upload_outliers
    upload_q1 = df["averageUpload"].quantile(0.25)
    upload_q3 = df["averageUpload"].quantile(0.75)
    upload_iqr = upload_q3 - upload_q1
    upload_lower_lim = upload_q1 - 1.5 * upload_iqr
    upload_upper_lim = upload_q3 + 1.5 * upload_iqr
    upload_outliers = (df["averageUpload"] < upload_lower_lim) + (df["averageUpload"] > upload_upper_lim)

    # outliers is True only if index is True in down_outliers and upload_outliers
    outliers = down_outliers * upload_outliers

    # Gets upload and download values for each outlier
    i = 0
    outliers_values = pd.DataFrame()
    while i < len(df):
        if outliers.iloc[i]:
            outliers_values = pd.concat([pd.DataFrame({"averageDown": [df.iloc[i]["averageDown"]],
                                                       "averageUpload": [df.iloc[i]["averageUpload"]]}),
                                         outliers_values], ignore_index=True)
        i += 1

    # Calculates correlation coefficient
    correlation = df["averageDown"].corr(df["averageUpload"])

    # Calculates regression line
    coefficient = np.polyfit(df["averageUpload"], df["averageDown"], 1)
    poly1d_fn = np.poly1d(coefficient)

    # Displays scatter points with label showing the correlation coefficient
    plt.plot(df["averageUpload"], df["averageDown"], "bo", label="Correlation: " +
                                                                 str('%.2f' % correlation))
    # Highlights outliers in red
    plt.plot(outliers_values["averageUpload"], outliers_values["averageDown"], "ro", label="Outliers")
    # Displays regression line
    plt.plot(df["averageUpload"], poly1d_fn(df["averageUpload"]), "orange", label="Regression Line")

    # Configuration settings to make plot clearer and more informative
    plt.title("Comparison of the relationship between broadband upload and\ndownload speeds in all regions of the UK")
    plt.legend(loc="lower right")
    plt.ylabel("Average download speed (Mb/s)")
    plt.xlabel("Average upload speed (Mb/s)")
    plt.xlim(0, 100)
    plt.ylim(0, 180)
    plt.grid()
    plt.show()

    main()


def time_ser_data():
    """
    Displays a line graph comparing the highest daily FTSE share index value over time. Calculates and displays a
    regression line.
    """
    df = pd.read_csv("C_financialData_2021/ftse_data_wrangled.csv")
    # Convert date data from string into date
    df["date"] = pd.to_datetime(df["date"])

    # Calculates regression line, use df.index to represent the date data
    coefficient = np.polyfit(df.index, df["High"], 1)
    poly1d_fn = np.poly1d(coefficient)

    plt.plot(df["date"], df["High"], "blue")
    # Displays regression line
    plt.plot(df["date"], poly1d_fn(df.index), "orange", label="Regression Line")

    # Configuration settings to make plot clearer and more informative
    plt.title("Comparison of the highest daily FTSE share index values over time")
    plt.legend(loc="lower right")
    plt.xlabel("Year")
    plt.ylabel("FTSE Share Index")
    plt.ylim(0, 8000)
    plt.grid()
    plt.show()

    main()


if __name__ == '__main__':
    main()
