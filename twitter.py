from twitterscraper import query_tweets
import datetime as dt
import pandas as pd
import os
from datetime import date
from calendar import monthrange
import numpy as np


def main():
    """iterates per 2 day of each month of each year and calls the twitter scraping function"""
    list_years = [2020, 2019, 2018, 2017, 2016]
    companies = ["tesla", "amazon", "apple", "netflix", "facebook", "microsoft", "google", "alphabet", "boeing"]
    for term in companies:
        print(f"Analyzing term: {term}")
        for year in list_years:
            if year == 2020:
                current_month = int(str(date.today()).split("-")[1].strip("0"))
                numerical_months = list(range(current_month + 1))
                del numerical_months[0]
            else:
                numerical_months = list(range(13))
                del numerical_months[0]
            for month in numerical_months:
                print(f"Current year: {year}, Month: {month}")
                num_days = int(str(monthrange(year, month)).split(", ")[1].replace(")", ""))
                lst = list(range(num_days + 1))
                del lst[0]
                lst.append(num_days - 1)
                lst = np.sort(lst)
                for day in lst:
                    if day == num_days:
                        if month + 1 == 13:
                            twitter_scraping_v3(day, 1, month, 1, year, year + 1, term)
                        else:
                            twitter_scraping_v2(day, 1, year, month, month + 1, term)
                    else:
                        twitter_scraping(day, day + 1, year, month, term)


def twitter_scraping_v3(first_day, second_day, first_month, second_month,
                        first_year, second_year, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""
    lang = "english"
    limit = 1000

    start = dt.date(first_year, first_month, first_day)
    end = dt.date(second_year, second_month, second_day)
    print(f"start: {start}/ end: {end} / {term}")

    tweets = query_tweets(term, begindate=start, limit=limit, enddate=end, lang=lang)
    df = pd.DataFrame(t.__dict__ for t in tweets)

    save_df(df, term)


def twitter_scraping_v2(first_day, second_day, year, first_month, second_month, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""
    limit = 1000
    lang = "english"

    start = dt.date(year, first_month, first_day)
    end = dt.date(year, second_month, second_day)
    print(f"start: {start}/ end: {end} / {term}")

    tweets = query_tweets(term, begindate=start, limit=limit, enddate=end, lang=lang)
    df = pd.DataFrame(t.__dict__ for t in tweets)

    save_df(df, term)


def twitter_scraping(first_day, second_day, year, month, term):
    """gets called per 2 sets of days for the start and end parameter of the
    twitter scraper function"""
    limit = 1000
    lang = "english"

    start = dt.date(year, month, first_day)
    end = dt.date(year, month, second_day)
    print(f"start: {start}/ end: {end} / {term}")

    tweets = query_tweets(term, begindate=start, limit=limit, enddate=end, lang=lang)
    df = pd.DataFrame(t.__dict__ for t in tweets)

    save_df(df, term)


def save_df(dataframe, term):
    """checks to see if an existing csv file exists if it does it'll update it with the new
        articles and if it does not it will create a new csv file for the company"""
    if os.path.exists(f"E:\\Tweet Data\\tweets {term}.csv"):
        existing_df = pd.read_csv(f"E:\\Tweet Data\\tweets {term}.csv")
        updated_df = existing_df.append(dataframe, ignore_index=True)
        no_duplicated_df = updated_df.drop_duplicates('tweet_url', keep='last')
        no_duplicated_df.to_csv(f"E:\\Tweet Data\\tweets {term}.csv", mode='w', index=False)
    else:
        dataframe.to_csv(f"E:\\Tweet Data\\tweets {term}.csv", index=False)


main()
