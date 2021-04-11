from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import os
from datetime import datetime


def find_clinic_availability(driver, clinic):
    """
    Function that gathers time slots and appointments from valid/available clinics.
    The program then calls the export function to export all of this information.
    :param driver: Driver session passed in through main program.
    :param clinic: List of valid clinic links from find_valid_clinics
    :return: None.
    """
    availability = {}
    try:
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        appt_blocks = table.find_elements_by_class_name("bg-gray-200")
        for appt_block in appt_blocks:
            time_slots = appt_block.find_elements_by_tag_name("span")
            slot_availability = appt_block.find_elements_by_tag_name("p")
            for time_slot in time_slots:
                for slot in slot_availability:
                    if slot.text[0] == "N":
                        availability[time_slot.text] = "0"
                    else:
                        availability[time_slot.text] = slot.text[0]
        time_slots = list(availability.keys())
        appointments = list(availability.values())
        export(time_slots, appointments, clinic)

    except:
        return


def find_valid_clinics(driver):
    """
    Program to gather links for available clinics and compile them into a list.
    :param driver: Driver session passed in through main program.
    :return: List of available clinic links.
    """
    links = []
    vc = driver.find_elements_by_link_text("Sign Up for a COVID-19 Vaccination")
    for clinic in vc:
        links.append(clinic.get_attribute('href'))
    return links


def fetch(driver, time_duration):
    """
    Fetching program to coordinate all other functions while True.
    :param driver: Driver session passed in through main program.
    :param time_duration: Time to reload program in seconds.
    :return: None.
    """
    start_url = "https://www.vaccinateri.org/clinic/search?page="
    page = 1

    driver.get(start_url + str(page))

    # Actively gets how many pages are available
    page_count = driver.find_elements_by_class_name("page")
    pages = int(len(page_count) - 2)

    while True:
        valid_clinics = find_valid_clinics(driver)
        for clinic in valid_clinics:
            driver.get(clinic)
            find_clinic_availability(driver, clinic)
            driver.back()

        page += 1

        if page > pages:
            print("debugging")
            if time_duration != '':
                time.sleep(int(time_duration))
                print("Starting again")
                print(driver)
                fetch(driver, time_duration)
            else:
                # No time duration specified e.x: one-time data-grab
                break
        else:
            driver.get(start_url + str(page))


def export(time_slots, appointments, clinic):
    """
    Program to export all vaccination appointments into a specified CSV folder.
    :param time_slots: Time slots per vaccination clinic.
    :param appointments: Number of appointments per vaccination clinic.
    :param clinic: Unique clinic ID for each available clinic.
    :return: A CSV file per clinic containing all of the above variable information.
    """
    clinic = clinic.split("?")[1]
    # Compiling Appointment Findings...
    info_details = {'time slot': time_slots, 'appointments': appointments}
    # Creating DataFrame
    info_df = pd.DataFrame(info_details)
    # Getting current date and time...
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M")
    # Exports all Info to a CSV file at the following path (path of project files):
    info_df.to_csv(str(clinic) + "_" + str(dt_string) + '.csv', index=False)
