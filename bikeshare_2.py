import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'none']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    print('\nData exists for the following cities: Washington, New York City, and Chicago.')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to see data for? ').lower()
    while city not in cities:
        print('\nOops, there is no database for the city you have chosen. Please check your spelling and try again')
        city = input('Would you like to see data for Washington, New York City, or Chicago? ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nIf you would like to filter the data by a specific month, please type in the month: January, Feburary, March, April, May, or June. Type "none" for no filter ').lower()
    while month not in months:
        print('\nOops, there is no data for {}. Please check your spelling and try again'.format(month))
        month = input('Would you like to see data for January, February, March, April, May, or June. Type "none" for no filter. ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nYou can also filter by day. If you would like to do so, please type in the day: Monday, Tuesday, Wednesday, etc... Type "none" for no day filter. ').lower()
    while day not in days:
        print('\nOops, there is no data for {}. Please check your spelling and try again'.format(day))
        day = input('If you would like to filter by day, please type in the day: Monday, Tuesday, Wednesday, etc... Type "none" for no day filter . ').lower()

    print('\nYou have chosen to look at the database of {}. We will filter month and day for {} and {}.'.format((city).capitalize(), day.capitalize(), month.capitalize()))

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
    # read in the database for the chosen city
    if city == 'washington':
        df = pd.read_csv('washington.csv')
        print('The bikeshare data for Washington has been loaded. ')
    elif city == 'new york city':
        df = pd.read_csv('new_york_city.csv')
        print('The bikeshare data for NYC has been loaded. ')
    elif city == 'chicago':
        df = pd.read_csv('chicago.csv')
        print('The bikeshare data for Chicago has been loaded. ')
    else:
        print('\nThere is no Bikeshare data for the chosen city. Please restart the program.')

    # If a filter was chosen, then filter database by user specified month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.strftime("%B")
    df['Day'] = df['Start Time'].dt.strftime("%A")
    type(df['Month'])

    if month == 'none':
        print('You have not chosen to filter by month. Data for all months will be displayed.')
    else:
        print('...filtering data by {}...'.format(month.capitalize()))
        df = df[df['Month'] == month.capitalize()]

    # If a day was chosen then filter database by user specified day
    if day == 'none':
        print('You have not chosen to filter by day. Data for all days will be displayed.')
    else:
        print('...filtering data by {}...'.format(day.capitalize()))
        df = df[df['Day'] == day.capitalize()]
        print('All Done!')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month 
    popular_month = df['Month'].mode()[0]

    print('\nThe most popular month of travel was {}.'.format(popular_month))

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print('\nThe most popular day of travel was {}.'.format(popular_day))

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.strftime("%I%p")
    popular_hour = df['Start Hour'].mode()[0]
    hour_counts = len(df[df['Start Hour'] == popular_hour].index)
    print('\nThe most popular start hour was {} with {} rentals starting.'.format(popular_hour, hour_counts))

    #print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    start_station_count = len(df[df['Start Station'] == popular_start_station].index)

    print('\nMost popular start station: {}\n'.format(popular_start_station))
    print('\nNumber of rentals starting at this station: {}\n'.format(start_station_count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    end_station_count = len(df[df['End Station'] == popular_end_station].index)

    print('\nMost popular end station: {}\n'.format(popular_end_station))
    print('\nNumber of rentals ending at this station: {}\n'.format(end_station_count))

    # display most frequent combination of start station and end station trip
    combi_count = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)[0]
    start, stop = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).index[0]
    print('\nThe most popular journey was from {} to {}.'.format(start, stop))
    print('It was carried out {} times'.format(combi_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = sum(df['Trip Duration'])

    # display mean travel time
    mean_time = total_time/len(df)
    print('\nThe total travel time was: {} seconds'.format(total_time))
    print('\nThe mean travel time was: {} seconds'.format(mean_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe count per user type is:\n', user_types)

    # Display counts of gender
    gender_counts = df['User Type'].value_counts()
    print('\nThe count per gender is:\n', gender_counts)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = int(min(df['Birth Year']))
        latest_yob = int(max(df['Birth Year']))
        mode_yob = int(df['Birth Year'].mode()[0])

        print('\nThe oldest bikeshare user was born in: ', earliest_yob)
        print('\nThe youngest bikeshare user was born in: ', latest_yob)
        print('\nMost bikeshare users were born in: ', mode_yob)

    else:
        print('There is no information about bikeshare users\' birth years in this dataset.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trips(df):
     """Displays individual trip data by 5 trips until user decides to stop."""

     yesorno = input('\nWould you like to see individual trip data? Yes or No? ').lower()
     for row in df.iterrows():
         if yesorno == 'yes':
             print(row)
             yesorno = input('\nWould you like to see the next trip? Yes or No? ').lower()
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
        individual_trips(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
