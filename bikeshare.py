import time
import pandas as pd
import numpy as np
import sys 

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
    #Initial information for user
	print('Hello! Let\'s explore some US bikeshare data!')
    
    # Ask if the user will explore the data
    answer = input('Would you like to see bikeshare data from Chicago, New York City, or Washington? Type in \'Yes\' or \'No\': ').lower()
    # If the user want to explore the data than ask the exact city
    if answer == 'yes':
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city_choice=True
        cities = ['chicago', 'new york city', 'washington']
        # while loop to check if city is available
		while city_choice:
            city = input('Please select, which of the three cities you like to explore. Type in Chicago, New York City, or Washington: ').lower()
            if city in cities:
                print(' ')
                print('Let\'s start with the data analysis of',city.title())
                city_choice=False
            else:
                print('That\'s not a valid city. Choose again!')
    # If not, close the program
    elif answer == 'no':
        print('Then maybe next time. Hope you come back soon')
        sys.exit()
    # If the input was not 'yes' or 'no' start again
    else:
        print('There was a mistake in your input. Let\'s start again')
        print(' ')
        main()
    
    print('and move on with the selection of time filters')
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month_choice=True
    months_select = ['all','january', 'february', 'march','april','may','june']
    while month_choice:
        month = input('Do you want to analyze a specific month (january - june) or all months? Type in a specific month or the word \'all\': ').lower()
        if month in months_select:
            print('Let\'s start with the analysis of the specific period:',month.title())
            month_choice=False
        else:
            print('That\'s not a valid period (only months between january and june are allowed). Choose again!')
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_choice=True
    days_select = ['all','monday', 'tuesday', 'wednesday','thursday','friday','saturday','sunday']
    while day_choice:
        day = input('Do you want to analyze a specific day of the week (e.g., Tuesday) or all days of a week? \nType in a specific day or the word \'all\': ').lower()
        if day in days_select:
            day_choice=False
        else:
            print('That\'s not a valid day selection. Choose again!')

    print('-'*40)
    print('Your selection for the analysis:','\ncity:',city.title(),'\nmonth:',month.title(),'\nday of the week:',day.title())
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
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    #Control df
    #print(df)
    
    return df


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, if all months were selected
    # If a specific month was choosen (!= all) than give the choosen month back
    if month == 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = df['month'].mode()[0] - 1
        popular_month = months[popular_month] 
        print('Most popular month in',city.title(),'is:', popular_month.title())
    elif month != 'all':
        print('Note: Most popular month in the analysis is the selected month:', month.title())    
    
    print(' ')
    
    # display the most common day of week, if all days of the week were selected
    # If a specific day was choosen (!= all) than give the choosen day back
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most popular day in',city.title(),'is:', popular_day)
      
    elif day != 'all':
        print('Note: Most popular day in the analysis is the selected day:', day.title())
        
    print(' ')
    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts().max()
    print('Most Popular Start Hour:', popular_hour,'with',count_hour,'counts.')
    
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count_start_station = df['Start Station'].value_counts()[0].max()
    print('Most popular start station:', popular_start_station, 'with',count_start_station,'counts.')
    print(' ')
    
    # display most commonly used end station    
    popular_end_station = df['End Station'].mode()[0]
    count_end_station = df['End Station'].value_counts()[0].max()
    print('Most popular end station:', popular_end_station, 'with',count_end_station,'counts.')
    print(' ')
    
    # display most frequent combination of start station and end station trip
    # Concate start and end stations
    combi_start_end = df['End Station'] + ' and ' + df['Start Station']   
    popular_combi_station = combi_start_end.mode()[0]
    count_combi_station = combi_start_end.value_counts()[0].max()
    print('Most popular combination of start and end station:', popular_combi_station, 'with',count_combi_station,'counts.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = int(df['Trip Duration'].sum())
    #calculate total travel time in hours
    total_time_hour = int(total_time/3600)
    print('The total travel time is', total_time, 'seconds.')
    print('These are', total_time_hour, 'hours of bikeshare use.')
    print(' ')
    
    # display mean travel time
    mean_time = int(df['Trip Duration'].mean())
    print('The mean travel time is', mean_time, 'sec.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('These are the counts of each user type in',city.title())
    print(user_types)
    print(' ')
    
    # Display counts of gender
    if city == 'washington':
        print ('Note: There are no information of the gender available in the data of',city.title())
    else:
        gender = df['Gender'].value_counts()
        print('These are the counts of each gender in:',city.title())
        print(gender)
    print(' ')
    
    # TO DO: Display earliest, most recent, and most common year of birth
    # Give user information that gender is not available in Washington
    if city == 'washington':
        print ('Note: There are no information of the birth year available in the data of',city.title())
    else:
        #calculate earliest date
        earliest_date = int(df['Birth Year'].min())
        #calculate recent date
        recent_date = int(df['Birth Year'].max())
        #calculate common date
        common_date = int(df['Birth Year'].mode()[0])
        print('The birth year of the oldest user:', earliest_date)
        print('The birth year of the youngest user:',recent_date)
        print('The most common birth year of the users:',common_date)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data on bikeshare users."""
    raw_choice=True
    while raw_choice:
    # Ask if the user will explore the first 5 lines or raw data
        answer_data = input('Do you want to see 5 lines of raw data? Type in \'Yes\' or \'No\': ').lower()
		# If the user want to explore the data than show the first 5 lines
        if answer_data == 'yes':
            print(df.iloc[:5])
            raw_choice_sub=True
            n=10
            while raw_choice_sub:
                # If the user want to explore more data than show 5 lines extra
                answer_data_sub = input('Do you want to see more lines of raw data? Type in \'Yes\' or \'No\': ').lower()
                if answer_data_sub == 'yes':
                    print(df.iloc[(n-5):n])
                    n+=5
                elif answer_data_sub == 'no':
                    raw_choice_sub=False
                    raw_choice=False
            
        elif answer_data == 'no':
            raw_choice=False
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
		
		# different functions available for analysis
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
