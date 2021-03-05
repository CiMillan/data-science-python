import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nWould you like to see data from Chicago, New York, or Washington?\n").lower()
    while city not in ('chicago', 'new york', 'washington'):
        print("Sorry, I didn't catch that.")
        city = input("\nWould you like to see data from Chicago, New York, or Washington?\n").lower()
    # get user input for time filter
    time_filter = input("\nWould you like to filter the data by month, day, or not at all? Type 'all' for no time filter.\n").lower()
    while time_filter not in ('month', 'day', 'all'):
        print("Sorry, I didn't catch that.")
        time_filter = input("\nWould you like to filter the data by month, day, or not at all? Type 'all' for no time filter.\n").lower()
    # get user input for month (all, january, february, ... , june)
    if time_filter == "month":
        month = input("\nWhich month? January, February, March, April, June, or all?\n").lower()
        while month not in ('january', 'february', 'march', 'april', 'june', 'all'):
            print("Sorry, I didn't catch that.")
            month = input("\nWhich month? January, February, March, April, June, or all?\n").lower()
        day = "all"
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif time_filter == "day":
        day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n").lower()
        while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Sorry, I didn't catch that.")
            day = input("\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n").lower()
        month = "all"
    else:
        day = "all"
        month = "all"

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    #Filter by day of week if applicable
    if day != 'all':
        #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['month'].mode()[0]
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hou
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Month:', popular_month)
    print('Most Popular Day of week:', popular_day)
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    popular_trip = df['Start To End'].mode()[0]

    print('Most Popular Start Station:', popular_start)
    print('Most Popular End Station:', popular_end)
    print('Most Popular Trip:', popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_duration = df['Trip Duration'].sum()
    # display mean travel time
    avg_time = round(df['Trip Duration'].mean())
    print('Total Travel Time:', total_duration)
    print('Average Trip Duration:', avg_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user = df['User Type'].value_counts()
    print('\nUser types count:\n', user)
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('\nGender count:\n', gender)
    except:
        print("\nNo gender records available for this location.")
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest year of birth:', earliest_year)
        print('\nMost recent year of birth:', recent_year)
        print('\nMost common year of birth:', common_year)
    except:
        print("\nNo birth records available for this location.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Asks user whether he wants to see 5 rows of data."""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower()
    start_loc = 0
    while view_data == "yes":
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5  
        view_display = input("Do you wish to continue?: ").lower()
        if view_display.lower() != "yes":
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
