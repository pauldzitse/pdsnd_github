#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['chicago', 'new york city', 'washington']
    months = ['all','january', 'february','march', 'april', 'may', 'june']
    days = ['all', 'sunday','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    # gives the user the first information
    print('Hello welcome, we\'re going to explore some US bikeshare data. The research centres on these cities: chicago, new york city and washington.')

    # get user input for city (chicago, new york city, washington) and handle invalid inputs
    while True:
        try:
            city = str(input('\nEnter the name of a city you want explore: '))
            if city in cities:
                print('\nFantastic!\n')
                break
            elif city not in cities:
                print('\nCity not found, please retry!\n ')
        except:
            pass

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Enter a month from january to june, otherwise enter "all" to apply no filter: ')
            if month in months:
                print('\nBravo!\n')
                break
            elif month not in months:
                print('Month not found, please retry!\n ')
        except:
            pass

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Enter a day between sunday to saturday, otherwise enter "all" to apply no filter: ')
            if day in days:
                print('\nExcellent!\n')
                break
            elif day not in days:
                print('Day not found, please retry!\n')
        except:
            pass


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and days
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the START TIME column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Here the displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month:', int(most_common_month))

    # display the most common day of week
    most_commmon_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', most_commmon_day)

    # display the most common start hour
    most_common_start_hour = int(df['hour'].mode()[0])
    print('The most commmon start hour: {}:00'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station: ", most_common_end_station)

    # display most frequent used start and end station
    df['Comomn Combination'] = df['Start Station']+' | | ' +df['End Station']
    most_frequent_combination = df['Comomn Combination'].value_counts().idxmax()
    print('The most frequent combination of start station and end station trip: ', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total duration of time travel is {} seconds '.format(total_travel_time))

    # display mean travel time
    mean_time_travel = df['Trip Duration'].mean()
    print('The mean time travel is {} seconds '.format(mean_time_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_type_count = df['User Type'].value_counts()

    # display counts of subscriber user types
    subscrib_user_count = user_type_count.iloc[0]
    print('There are {} suscriber users'.format(subscrib_user_count))

    # display counts of customer types
    customer_user_count = user_type_count.iloc[1]
    print('There are {} customer users'.format(customer_user_count))

    # display counts of nonuser types
    nouser_type_count = df['User Type'].isnull().sum()
    print('There are {} unidentified users'.format(nouser_type_count))

    # display gender counts
    if  'Gender' in df:
        gender_type_count = df['Gender'].value_counts()

        male_count = gender_type_count.iloc[0]
        print('There are {} males'.format(male_count))

        female_count = gender_type_count.iloc[1]
        print('There are {} females'.format(female_count))

        nogender_type_count = df['Gender'].isnull().sum()
        print('There are {} genders unidentified'.format(nogender_type_count))
    else:
        print('There is no Gender information on this city')

    # display earliest, most recent, and most common year of birth
    if  'Birth Year' in df:
        earliest_year_birth = df['Birth Year'].min()
        print('The earliest birth year:', int(earliest_year_birth))

        most_recent_year_birth = df['Birth Year'].max()
        print('The recent birth year:', int(most_recent_year_birth))

        most_common_year_birth = df['Birth Year'].mode()[0]
        print('The most common year birth:', int(most_common_year_birth))

    else:
        print('There is no birth information for your selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays raw data on bikeshare users."""

    i = 0
    j = 5
    while True:
        user_wish = input('\nWould you like to view data? Enter yes or no\n\n')
        if user_wish == 'yes':
            print('\nFive rows printed!\n',df.iloc[i:j])
            i += 5
            j += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
