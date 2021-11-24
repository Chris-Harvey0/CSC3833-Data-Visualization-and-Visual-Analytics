import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    """
    Main method
    """

    cat_data()
    num_data()
    time_ser_data()


def cat_data():
    """
    Displays two bar charts to compare four categories of housing and their prices in two regions of the UK.
    """

    df = pd.read_csv("A_housePriceData_2021/Average-prices-Property-Type-2021-05_wrangled.csv")

    # Separates the data by region and does not add unnecessary rows
    london_df = df[df["Region_Name"].isin(["London"])]
    newcastle_df = df[df["Region_Name"].isin(["Newcastle upon Tyne"])]

    average_prices = []
    for region_df in london_df, newcastle_df:
        for value in ["Detached", "Semi_Detached", "Terraced", "Flat"]:
            average_prices.append(region_df[region_df["propertyType"].isin([value])]["averagePrice"].mean()/1000)

    # Adding the bar chart
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    fig.suptitle("Comparison of four categories of housing and their prices in two\nregions of the UK")
    x = np.arange(4)
    bar_width = 0.4
    ax.bar(x, list(average_prices[:4]), color="blue", width=bar_width, label="London")
    ax.bar(x + bar_width, average_prices[4:], color="orange", width=bar_width, label="Newcastle upon Tyne")

    # Configuration settings to make plots clearer and more informative
    plt.legend(loc="upper right")
    ax.set_ylabel("Average price in thousands (£)")
    ax.set_ylim(0, 700)
    ax.yaxis.grid()
    ax.set_xticks(x + bar_width/2)
    ax.set_xticklabels(["Detached", "Semi-Detached", "Terraced", "Flat"])
    plt.show()


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


if __name__ == '__main__':
    main()
