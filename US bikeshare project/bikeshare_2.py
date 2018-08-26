import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    city = input("Choose the city you want to see data from : chicago, new york city, washington\n ").lower()

    print("Please choose all for no filtering.")

    # get user input for month (all, january, february, ... , june)
    month = input("Which month's data you want to see? Please choose from All, January, February, March, April, May, June.\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day_int = int(input("Choose the day of the week: Please give it as an integer. (e.g., All-0,Monday-1...Sunday-7)\n"))
    day_list = ['All','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = day_list[day_int]
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
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = df['month'].value_counts().index[0]

    print("Most Common Month : {}".format(months[most_common_month-1]))

    # display the most common day of week

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    most_common_day = df['day_of_week'].value_counts().index[0]
    print("Most Common day : {}".format(days[most_common_day]))


    # display the most common start hour


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start_station = df['Start Station'].value_counts().index[0]
    print("The most common Start Station is : {}".format(popular_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().index[0]
    print("The most common End Station is : {}".format(common_end_station))
    # display most frequent combination of start station and end station trip
    most_common_pair = df.groupby(['Start Station','End Station']).max().index[0]
    print("most frequent combination of start station and end station is : {}".format(most_common_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    Total_duration = df['Trip Duration'].sum()
    print("Total trip duration :{}".format(Total_duration))

    # display mean travel time
    Mean_duration = df['Trip Duration'].mean()
    print("The mean travel time is :{}".format(Mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    try:
        print('\nCalculating User Stats...\n')
        start_time = time.time()

        # Display counts of user types
        user_type = df.groupby("User Type").size()
        print("Total count of each USER TYPE is : {}".format(user_type))
        # Display counts of gender
        gender_count = df.groupby("Gender").size()
        print("Total gender count is : {}".format(gender_count))


        # Display earliest, most recent, and most common year of birth
        earliest_birthyear = df['Birth Year'].sort_values(ascending = False).dropna().iloc[-1]
        most_recent_birthyear = df['Birth Year'].sort_values(ascending = False).iloc[0]
        most_common_year_of_birth = df['Birth Year'].value_counts().index[0]

        print("The earliest Birth Year : {}".format(earliest_birthyear))
        print("The most recent Birth Year : {}".format(most_recent_birthyear))
        print("The most common year of Birth is : {}".format(most_common_year_of_birth))


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    except Exception:
        print("User Details are not available for this city.")

def raw_data(df):
    count = 0
    while True:
        print(df[count : count+5])
        response = input("DO you want to see more? Yes or no.\n").lower()
        if response != 'yes':
            break




def main():
    pd.set_option('display.max_columns', 500)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print("\n")
        answer = input("DO you want to see raw_data? Please enter yes or no.\n")
        if answer == 'yes':
         raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
