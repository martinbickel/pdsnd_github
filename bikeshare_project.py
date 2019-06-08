import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': '/Users/acemartinb/Desktop/Udacity/Python/Project/bikeshare-2/chicago.csv',
              'new york city': '/Users/acemartinb/Desktop/Udacity/Python/Project/bikeshare-2/new_york_city.csv',
              'washington': '/Users/acemartinb/Desktop/Udacity/Python/Project/bikeshare-2/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze (Washington, New York City, Chicago)
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) decision_filter - kin of filter method: only by month, only by day, or both
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    month = ""
    day = ""
    while city not in CITY_DATA:
        city = input("Please choose one of the following cities (chicago, new york city or washington):  ").lower()
        if city not in CITY_DATA:
            print("There must be a mistake in your choice.")
            continue
        else:
            print("{} is a great decision!".format(city))
            break

    #gets the question what filters he wants to use
    filter_methods = ['day','month','both']
    decision_filter = ""
    while decision_filter not in filter_methods:
        decision_filter = input("Do you want to filter by day, month or both [please enter day,month or both]?: ".lower())
        if decision_filter not in filter_methods:
            print("There must be a mistake in your choice.")
            continue
        else:
            print("OK, we will filter by {}".format(decision_filter))
            break

    if decision_filter != 'day':
        # get user input for month (all, january, february, ... , june)
        month_right = False
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        while month_right != True:
            month = input("Please enter the month: ").lower()
            if month not in months:
                print("Are you sure thats a month you typed in?")
                continue
            else:
                month_right = True
                print("{} is a great decision!".format(month.title()))
                break

    if decision_filter != 'month':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day_right = False
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        while day_right != True:
            day = input("Please the name of the day you want to choose: ").lower()
            if day not in days:
                print("Are you sure that's the name of a day you typed in?")
                continue
            else:
                day_right = True
                print("{} is a great decision!".format(day.title()))
                break

    print('-'*40)
    return city, month, day, decision_filter


def load_data(city, month, day, decision_filter):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze (Either, Washington, Chicago or New York City)
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    df['day'] = df['Start Time'].dt.weekday_name
    if decision_filter != 'day':
        df = df[df['month'] == month[:3].title()]
    if decision_filter != 'month':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    months = {'Jan':'January','Feb':'February','Mar':'March','Apr':'April','May':'May','Jun':'June','Jul':'July','Aug':'August','Sep':'September','Oct':'October','Nov':'November','Dec':'December'}
    common_month = months[common_month]
    print("The most common month is {}.".format(common_month))

    # display the most common day of week
    common_day = df['day'].mode()[0]
    print("The most common day is {}".format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end))

    # display most frequent combination of start station and end station trip
    most_frequent= df[['Start Station','End Station']].mode()
    print("The most frequent combination is {} as a Start and {} as an End.".format(most_frequent['Start Station'][0], most_frequent['End Station'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    total_duration_hour = total_duration//3600
    total_duration_minutes = (total_duration%3600)//60
    total_duration_seconds = total_duration%60
    print("The total travel time was {} hours {} minutes and {} seconds.".format(total_duration_hour,total_duration_minutes, total_duration_seconds))

    # display mean travel time
    mean_duration = int(df['Trip Duration'].mean())
    print("The mean duration was {} seconds.".format(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The types of users are split in the following numbers:\n",user_types)

    if city != 'washington':
        # Display counts of gender
        gender_types = df['Gender'].value_counts()
        print("The types of gender among the users are split in the following numbers:\n",gender_types)

        # Display earliest, most recent, and most common year of birth
        earliest_byear = int(df['Birth Year'].min())
        recent_byear = int(df['Birth Year'].max())
        common_byear = int(df['Birth Year'].mode()[0])
        print("The earliest, the most recent and the most common year of birth is {}, {} and {}.".format(earliest_byear,recent_byear, common_byear))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def show_raw_data(df):
    """shows five lines of raw data. It is possible to scroll through the data by entering next or before"""
    decision_show = False
    while True:
        show_raw = input("Do you want to see the first 5 lines of the raw data? (y,n): ")
        if show_raw == "n":
            break
        elif show_raw == "y":
            decision_show = True
            print(decision_show)
            break
        else:
            print("oops, did you really enter y or n?")
            continue
    raw_start = 0
    raw_end = 5
    if decision_show == True:
        while True:
            raw_data = df[raw_start:raw_end]
            print('-'*40)
            print(raw_data)
            print('-'*40)
            if raw_end <= 5:
                decision_raw = input("Do you want to see the next 5 lines or end? (next, end): ").lower()
            else:
                decision_raw = input("Do you want to see the next or the 5 lines before or end? (next,before, end): ").lower()

            if decision_raw in ['next','before','end']:
                if decision_raw == 'next':
                    raw_start += 5
                    raw_end += 5
                    continue
                elif decision_raw == 'before':
                    raw_start -= 5
                    raw_end -= 5
                elif decision_raw == 'end':
                    break
            else:
                print('-'*40)
                print("\nMust be a mistake in your answer. Please try again!\n")
                print('-'*40)
                continue


def main():
    while True:
        city, month, day, decision_filter = get_filters()
        df = load_data(city, month, day, decision_filter)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for analyzing the bike data base!")
            break


if __name__ == "__main__":
	main()
