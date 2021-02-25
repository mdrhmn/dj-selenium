# Django
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
import os

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from django.contrib import messages

def autologin(driver, url, username, password):
    driver.get(url)
    password_input = driver.find_element_by_xpath("//input[@type='password']")
    password_input.send_keys(password)
    username_input = password_input.find_element_by_xpath(
        ".//preceding::input[not(@type='hidden')]")
    username_input.send_keys(username)
    form_element = password_input.find_element_by_xpath(".//ancestor::form")
    submit_button = form_element.find_element_by_xpath(
        ".//*[@type='submit']").click()
    return driver


def scrap(request):

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    autologin(driver, 'https://maya.um.edu.my/sitsvision/wrd/siw_lgn',
              USERNAME, PASSWORD)

    timetable_popup = driver.find_element_by_xpath(
        "//a[@href='javascript:timetable_popup();']").click()

    search_timetable = driver.find_element_by_xpath(
        "//*[@id='sits_dialog']/center/div/div/div[3]/a").click()

    login_id = driver.find_element_by_xpath('//*[@id="poddatasection"]/div[2]/div[2]/div/div/fieldset/div[2]/label').get_attribute("for")
    login_id_modified = login_id.removesuffix('.1-1').replace(".", "_")
    login_id_truncated = login_id.removesuffix('.1-1')

    select_year_dropdown = driver.find_element_by_xpath("//*[@id='" + login_id_modified + "_1_1_chosen']/a").click()
    select_year = driver.find_element_by_xpath("//*[@id='" + login_id_truncated + ".1-111']").click()

    select_semester_dropdown = driver.find_element_by_xpath("//*[@id='" + login_id_modified + "_2_1_chosen']/a").click()
    select_semester = driver.find_element_by_xpath("//*[@id='" + login_id_truncated + ".2-120']").click()

    select_faculty_dropdown = driver.find_element_by_xpath("//*[@id='" + login_id_modified + "_3_1_chosen']/a").click()
    select_faculty = driver.find_element_by_xpath("//*[@id='" + login_id_truncated + ".3-121']").click()

    select_campus = Select(driver.find_element_by_id(login_id.removesuffix('.1-1') + '.5-1'))
    select_campus.select_by_visible_text('UNIVERSITI MALAYA KUALA LUMPUR')

    submit_timetable = driver.find_element_by_xpath("//*[@id='poddatasection']/div[2]/div[3]/div/input[3]").click()

    last_page = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_last']/a")
    driver.execute_script("arguments[0].click();", last_page)
    last_page_num = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_paginate']/ul/li[7]/a").get_attribute('text')
    first_page = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_first']/a")
    driver.execute_script("arguments[0].click();", first_page)
    table_element = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_wrapper']")
    
    if not os.path.exists("maya.txt"):
        f = open("maya.txt", "a")
    else:
        f = open("maya.txt", "a")
    for i in range (int(last_page_num)):
        for tr in table_element.find_elements_by_tag_name('tr'):

            if tr.get_attribute('class') == '' or tr.get_attribute('class') == None:
                f.write("PAGE " + str(i + 1) + "\n\n")
                f.write(tr.text)
            else:
                f.write(tr.text)

            f.write("\n\n")

        next_page = driver.find_element_by_xpath("//*[@id='DataTables_Table_0_next']/a")
        driver.execute_script("arguments[0].click();", next_page)

    f.close()

    driver.quit()
    messages.success(request, "Timetable extraction successful.")
    return HttpResponseRedirect('/main/')
