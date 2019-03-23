#Stephen_H_Bikeshare_Project/bikeshare_2.py

import platform
import os
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    city = ''

    while True:
        city = input('\nChoose a city between Chicago, New York City, and Washington:\n> ').lower()
        if city not in cities:
            print('\n\'{}\' is not found in our records.'.format(city))
            continue
        else:
            break

    month = ''

    while True:
        month = input('\nWhat month would you like to filter your data by?  \nJanuary, February, March, April, May, or June?.  \nType All to filter data by all months.\n> ').lower()
        if month not in months:
            print('\n\'{}\' is not found in our records.'.format(month))
            continue
        else:
            break

    day = ''

    while True:
        day = input('\nWhat day would you like to filter your data by?  \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?  \nType All to filter by all days.\n> ').lower()
        if day not in days:
            print('\n\'{}\' is not found in our records.'.format(day))
            continue
        else:
            break


    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    popular_month = df['month'].mode()[0]
    print('Most Popular Month: {}'.format(popular_month))

    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.day

    popular_day = df['day'].mode()[0]
    print('Most Popular Day: {}'.format(popular_day))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station: {}'.format(popular_start_station))
    print('Start Station Counts: {}\n'.format(df['Start Station'].value_counts()[popular_start_station]))

    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station: {}'.format(popular_end_station))
    print('End Station Counts: {}\n'.format(df['End Station'].value_counts()[popular_end_station]))

    # find most frequent combination of start station and end station trip
    total_trip = df['Start Station'] + ' - ' + df['End Station']

    most_frequent_trip = total_trip.mode()[0]
    print('Most Frequent Trip: {}'.format(most_frequent_trip))
    print('Frequent Trip Counts: {}'.format(total_trip.value_counts()[most_frequent_trip]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {}'.format(total_travel_time))

    avg_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time: {}'.format(avg_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays user statistics such as user type, gender, and birth year on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Types: \n{}\n'.format(user_types))

    # This try/exception code block handles KeyErrors for Washington filter
    # Washington csv does not have Gender or Birth Year columns
    try:
        gender_types = df['Gender'].value_counts()

        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        popular_birth_year = df['Birth Year'].mode()[0]
    except KeyError:
        print('Gender column not available. \nCannot display statistics.\n')

        print('Birth Year column not available.  \nCannot display statistics.')
    else:
        print('Gender Types: \n{}\n'.format(gender_types))

        print('Earliest Birth Year: {}'.format(int(earliest_birth_year)))
        print('Recent Birth Year: {}'.format(int(recent_birth_year)))
        print('Most Popular Birth Year: {}'.format(int(popular_birth_year)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """ Accesses csv doc and displays 5 rows of its raw data at a time """

    raw_data_prompt = input('\nWould you like to see 5 rows of raw data?  (Yes or No)\n> ').lower()

    if raw_data_prompt == 'yes':
        print('\nAccessing Raw Data...\n')
        start_time = time.time()

        # i = index location
        i = 0
        while True:
            # select 5 rows inside csv and print rows of raw data
            print(df.iloc[i:i + 5])
            i += 5

            print("\nThis took %s seconds." % (time.time() - start_time))
            print('-'*40)

            more_raw_data = input('\nWould you like to see 5 more rows of raw data?  (Yes or No)\n> ').lower()
            if more_raw_data != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)


        restart_app = input('\nWould you like to restart?  (Yes or No)\n> ')
        if restart_app.lower() == 'yes':
            os_type = platform.system()
            # Darwin is the system name for macOS
            if os_type in ('Darwin', 'Linux'):
                os.system('clear')
            elif os_type == 'Windows':
                os.system('cls')
            else:
                continue
        elif restart_app.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
