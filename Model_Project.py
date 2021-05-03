# Imports
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
from matplotlib import pyplot
import statistics as stats
import os
import time


# Model to predict based on week
def fetch_day():
    # Load the data for the specified day
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    dates = ["04/11/2021", "04/12/2021", "04/13/2021", "04/14/2021", "04/15/2021", "04/16/2021", "04/17/2021"]

    # Initializing
    totals = []
    total_appointments = []
    total_daily = []

    for day in days:
        path = "Data/" + day + "/"
        dirs = (os.listdir(path))

        for folders in dirs:
            # Once all folders for that time instance are gathered, get data
            folder_path = folders + "/"
            files = os.listdir(path + folder_path)
            # For each folder for that time instance, gather data

            for file in files:
                current_path = path + folder_path + file
                # Goes through each CSV file in the folder
                read = pd.read_csv(current_path)

                # Cleaning each file (will be made into sep. cleaning function)
                read = read[read["time slot"] != 'Add To Waiting List']

                # Making all appointment values numeric - caused an issue with whitespace before
                read["appointments"] = read["appointments"].apply(pd.to_numeric)

                # Total # of appointments for each instance
                total = int(read["appointments"].sum())
                totals.clear()
                totals.append(total)

                # Getting all appointments for user-indicated time - STRETCH GOAL
                # info_df = info_df.append(read[read["time slot"] == time_range], ignore_index=True)

            total_appts = sum(totals)
            total_appointments.append(total_appts)

        total_for_day = sum(total_appointments)
        total_appointments.clear()
        total_daily.append(total_for_day)

    # Return DF with day of the week and total number of appointments
    info_df = pd.DataFrame({"date": dates,
                            "appointments": total_daily})

    # Returns a CSV file to be used as input to forecasting model with data from specified user input
    print("Done fetching...")
    return info_df


def ARIMA_day():
    # Walk-forward validation with ARIMA
    # load dataset
    data = pd.read_csv("info.csv", index_col="date")
    data.index = pd.to_datetime(data.index).to_period('D')

    # Split into train and test sets
    X = data.values
    size = int(len(X) * 0.45)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()

    # Walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=(0, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)

    # Return prediction
    print('predicted= ', predictions)

    # Evaluate forecasts
    rmse = sqrt(mean_squared_error(test, predictions))
    print('Test RMSE: %.3f' % rmse)

    # Plot forecasts against actual outcomes
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.savefig("image.png")


# Model to predict based on hour of the day
def fetch_hour(day, start_time, end_time):
    # Load the data for the specified day
    path = "Data/" + str(day) + "/"
    dirs = (os.listdir(path))

    # Initializing
    time_range = list(range(int(start_time), int(end_time)))
    time_formatted = []
    folders = []
    totals = []
    total_appointments = []
    total_by_hour = []

    for times in time_range:
        # Gets time in seconds for model
        time_formatted.append(time.strftime('%H:%M:%S', time.gmtime(times * 3600)))
        for directory in dirs:
            full_path = directory + "/"
            # Getting time that the folder was created
            time_tuple = time.strptime(time.ctime(os.path.getmtime(path + full_path)))
            if int(time_tuple[3]) == int(times):
                folders.append(directory)

        for folder in folders:
            # Once all folders for that time instance are gathered, get data
            folder_path = folder + "/"
            files = os.listdir(path + folder_path)

            # For each folder for that time instance, gather data
            for file in files:
                current_path = path + folder_path + file
                # Goes through each CSV file in the folder
                read = pd.read_csv(current_path)

                # Cleaning each file (will be made into sep. cleaning function)
                read = read[read["time slot"] != 'Add To Waiting List']

                # Making all appointment values numeric - caused an issue with whitespace before
                read["appointments"] = read["appointments"].apply(pd.to_numeric)

                # Total # of appointments for each instance
                total = int(read["appointments"].sum())
                totals.append(total)

            total_appts = sum(totals)
            totals.clear()
            total_appointments.append(total_appts)

        total_hourly = int(stats.mean(total_appointments))
        total_by_hour.append(total_hourly)
        total_appointments.clear()

    # Return DF with times AND # appointments ONLY
    info_df = pd.DataFrame({"time_accessed": time_formatted,
                            "appointments": total_by_hour})

    # Returns a CSV file to be used as input to forecasting model with data from specified user input
    # info_df.to_csv('info.csv', index=False)
    print("Done fetching...")
    return info_df


def ARIMA_hour():
    # Walk-forward validation with ARIMA for hourly appointments
    # load dataset
    data = pd.read_csv("info.csv", index_col="time_accessed")
    data.index = pd.to_datetime(data.index).to_period('H')

    # Split into train and test sets
    X = data.values
    size = int(len(X) * 0.50)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()

    # Walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=(0, 1, 0))
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)

    # Return prediction
    print('predicted= ', predictions)

    # Evaluate forecasts
    rmse = sqrt(mean_squared_error(test, predictions))
    print('Test RMSE: %.3f' % rmse)

    # Plot forecasts against actual outcomes
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.savefig("image.png")
