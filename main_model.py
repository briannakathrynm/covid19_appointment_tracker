from Model_Project import fetch_day, fetch_hour, ARIMA_hour, ARIMA_day


def main():
    main_input = str(input("Enter whether to do predictions based on 'hour' or 'day': "))

    # Running each function
    if main_input == "hour":
        print("Enter day as follows: Monday, Tuesday, Wednesday, etc...")
        day = str(input("Enter a day for desired vaccination appointment: "))
        print("Enter time as follows: '10, 14' for 10am-2pm, etc...")
        time_range = str(input("Enter a time range in which you want to schedule your appointment: "))
        time_range = time_range.split(',')
        start_time = time_range[0]
        end_time = time_range[1]
        info = fetch_hour(day, start_time, end_time)
        info.to_csv('info.csv', index=False)
        ARIMA_hour()

    elif main_input == "day":
        info = fetch_day()
        info.to_csv('info.csv', index=False)
        ARIMA_day()


if __name__ == "__main__":
    main()
