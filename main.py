import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    """
    Main method
    :return: None
    :rtype: None
    """

    # Creates 4 subplots and sets figsize to 16:9
    fig, ax = plt.subplots(2, 2, figsize=[16, 9])
    cat_data(ax)
    num_data(ax)
    time_ser_data(ax)
    plot_description(ax)
    # Saves image to file with resolution of 1920x1080
    plt.savefig("CSC3833-State-of-the-Nation-Summative-Assignment.png", dpi=120)
    plt.show()


def cat_data(ax):
    """
    Displays a bar chart to compare four categories of housing and their prices in two regions of the UK.
    :param ax: Used to get or set some axis properties.
    :type ax: matplotlib.pyplot.axis
    :return: None
    :rtype: None
    """

    df = pd.read_csv("A_housePriceData_2021/Average-prices-Property-Type-2021-05_wrangled.csv")

    # Separates the data by region and does not add unnecessary rows
    london_df = df[df["Region_Name"].isin(["London"])]
    newcastle_df = df[df["Region_Name"].isin(["Newcastle upon Tyne"])]

    # Calculate average prices for each house type for each region
    average_prices = []
    for region_df in london_df, newcastle_df:
        for value in ["Detached", "Semi_Detached", "Terraced", "Flat"]:
            average_prices.append(region_df[region_df["propertyType"].isin([value])]["averagePrice"].mean() / 1000)

    ax[0, 0].set_title("Comparison of four categories of housing and their prices in two\nregions of the UK")
    x = np.arange(4)
    bar_width = 0.4
    ax[0, 0].bar(x, list(average_prices[:4]), color="blue", width=bar_width, label="London")
    ax[0, 0].bar(x + bar_width, average_prices[4:], color="orange", width=bar_width, label="Newcastle upon Tyne")

    # Configuration settings to make plots clearer and more informative
    ax[0, 0].legend(loc="upper right")
    ax[0, 0].set_ylabel("Average price in thousands (£)")
    ax[0, 0].set_ylim(0, 700)
    ax[0, 0].grid(axis="y")
    ax[0, 0].set_xticks(x + bar_width / 2)
    ax[0, 0].set_xticklabels(["Detached", "Semi-Detached", "Terraced", "Flat"])


def num_data(ax):
    """
    Displays a scatter graph comparing the relationship between broadband upload and download speeds in all regions of
    the UK. Calculates the correlation coefficient, regression line and outliers and displays these on the graph.
    :param ax: Used to get or set some axis properties.
    :type ax: matplotlib.pyplot.axis
    :return: None
    :rtype: None
    """

    df = pd.read_csv("B_broadbandData_2021/202006_fixed_laua_performance_wrangled.csv")

    down_outliers = find_outliers(df, "averageDown")

    upload_outliers = find_outliers(df, "averageUpload")

    # Combines the outliers for each axis and creates a dataframe with outliers removed
    outliers = df[down_outliers + upload_outliers]
    df_without_outliers = pd.concat([df, outliers]).drop_duplicates(keep=False)

    # Calculates correlation coefficient
    correlation = (df_without_outliers["averageDown"]).corr(df_without_outliers["averageUpload"])

    # Calculates regression line
    coefficient = np.polyfit(df_without_outliers["averageUpload"], df_without_outliers["averageDown"], 1)
    poly1d_fn = np.poly1d(coefficient)

    # Displays scatter points with label showing the correlation coefficient
    ax[0, 1].plot(df_without_outliers["averageUpload"], df_without_outliers["averageDown"], "bo",
                  label="Correlation: " + str('%.2f' % correlation))
    # Highlights outliers in red
    ax[0, 1].plot(outliers["averageUpload"], outliers["averageDown"], "ro", label="Outliers")
    # Displays regression line
    ax[0, 1].plot(df_without_outliers["averageUpload"], poly1d_fn(df_without_outliers["averageUpload"]), "orange",
                  label="Regression Line")

    # Configuration settings to make plot clearer and more informative
    ax[0, 1].set_title("Comparison of the relationship between broadband upload and\ndownload speeds in all regions "
                       "of the UK")
    ax[0, 1].legend(loc="lower right")
    ax[0, 1].set_ylabel("Average download speed (Mb/s)")
    ax[0, 1].set_xlabel("Average upload speed (Mb/s)")
    ax[0, 1].set_xlim(0, 100)
    ax[0, 1].set_ylim(0, 180)
    ax[0, 1].grid()


def find_outliers(df, column_name):
    """
    Finds all outliers not in the IQR for a column in a pandas dataframe
    :param df: pandas dataframe
    :type df: pandas.DataFrame
    :param column_name: Name of column in pandas dataframe
    :type column_name: String
    :return: dataframe containing all outliers from provided column
    :rtype: pandas.DataFrame
    """

    q1 = df[column_name].quantile(0.25)
    q3 = df[column_name].quantile(0.75)
    iqr = q3 - q1
    lower_lim = q1 - 1.5 * iqr
    upper_lim = q3 + 1.5 * iqr
    outliers = (df[column_name] < lower_lim) + (df[column_name] > upper_lim)

    return outliers


def time_ser_data(ax):
    """
    Displays a line graph comparing the highest daily FTSE share index value over time. Calculates and displays a
    regression line.
    :param ax: Used to get or set some axis properties.
    :type ax: matplotlib.pyplot.axis
    :return: None
    :rtype: None
    """

    df = pd.read_csv("C_financialData_2021/ftse_data_wrangled.csv")
    # Convert date data from string into date
    df["date"] = pd.to_datetime(df["date"])

    # Calculates regression line, use df.index to represent the date data
    coefficient = np.polyfit(df.index, df["High"], 1)
    poly1d_fn = np.poly1d(coefficient)

    ax[1, 0].plot(df["date"], df["High"], "blue")
    # Displays regression line
    ax[1, 0].plot(df["date"], poly1d_fn(df.index), "orange", label="Regression Line")

    # Configuration settings to make plot clearer and more informative
    ax[1, 0].set_title("Comparison of the highest daily FTSE share index values over time")
    ax[1, 0].legend(loc="lower right")
    ax[1, 0].set_xlabel("Year")
    ax[1, 0].set_ylabel("FTSE Share Index")
    ax[1, 0].set_ylim(0, 8000)
    ax[1, 0].grid()


def plot_description(ax):
    """
    Short narrative describing the main takeaway of each of the three plots.
    :param ax: Used to get or set some axis properties.
    :type ax: matplotlib.pyplot.axis
    :return: None
    :rtype: None
    """

    text = "Figure A:\n" \
           "This plot demonstrates the difference in house prices between London and \n" \
           "Newcastle upon Tyne across four categories of housing. The main takeaway from \n" \
           "this plot is that housing in London is at least double the price of housing in \n" \
           "Newcastle upon Tyne for all categories and for some categories it is almost triple.\n" \
           "\n" \
           "Figure B:\n" \
           "This plot demonstrates the relation between average download speed and average \n" \
           "upload speed. This plot shows there is a significant positive correlation between \n" \
           "the two variables. The correlation coefficient of 0.73 is significant, however a \n" \
           "number of outliers needed removing to reach this number.\n" \
           "\n" \
           "Figure C:\n" \
           "This plot shows the change in the FTSE Share Index over time from 1984 to 2021. \n" \
           "There is clearly some volatility in the value displayed, but the regression line \n" \
           "clearly shows there is a steady increase over time."

    # Sets x and y padding for the text
    ax[1, 1].text(0.05, 0.15, text, fontsize=9)
    # Removes the xticks and yticks from the plot
    ax[1, 1].set_xticks([])
    ax[1, 1].set_yticks([])


if __name__ == '__main__':
    main()
