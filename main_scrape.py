from selenium import webdriver
from Project import webscrapetest

driver = 0

def main():
    """
    Main function to drive program, takes input of "time_duration" from user.
    See notes at bottom for any tasks to be completed. Make sure that the file structure for
    these programs is as follows:
    > Outer_Folder
        > main_scrape.py
        > Inner_Folder
            > webscrapetest.py
    :return:
    """
    global driver
    #~! Enter your driver for your computer HERE !~#
    driver = webdriver.Chrome("ENTER_YOUR_PATH_HERE")
    driver.delete_all_cookies()

    time_duration = str(input("Enter 'x' to run program continuously every 'x' seconds: "))
    print(driver)
    webscrapetest.fetch(driver, time_duration)

if __name__ == "__main__":
    main()

#! Notes
# Automate for different time instances, run every 5 min or 1 min etc in sep. csv files -- done
# Add time to filename or create directory for each time -- done
