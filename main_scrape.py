from selenium import webdriver
from Project import webscrapetest

# Initializing driver instance
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
    path = str(input("Enter file path for driver.exe here: "))
    driver = webdriver.Chrome(path)
    driver.delete_all_cookies()

    time_duration = str(input("Enter 'x' to run program continuously every 'x' seconds. If enter key is pressed, "
                              "program will default to 60 seconds: "))
    if time_duration == "":
        time_duration = 60

    webscrapetest.fetch(driver, time_duration)

if __name__ == "__main__":
    main()
