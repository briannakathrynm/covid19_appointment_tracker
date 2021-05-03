from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def find_clinic_availability(driver):
    availability = {}

    try:
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        # table = driver.find_element_by_tag_name("table")
        appt_blocks = table.find_elements_by_class_name("bg-gray-200")
        for appt_block in appt_blocks:
            time_slots = appt_block.find_elements_by_tag_name("span")
            slot_availability = appt_block.find_elements_by_tag_name("p")
            for time_slot in time_slots:
                # print(time_slot.text)
                for slot in slot_availability:
                    if slot.text[0] == "N":
                        availability[time_slot.text] = "0"
                    else:
                        availability[time_slot.text] = slot.text[0]

        print(availability)
        return availability

    except NoSuchElementException:
        return


def find_valid_clinics(driver):
    links = []
    vc = driver.find_elements_by_link_text("Sign Up for a COVID-19 Vaccination")
    for clinic in vc:
        links.append(clinic.get_attribute('href'))
        print(links)
    return links
