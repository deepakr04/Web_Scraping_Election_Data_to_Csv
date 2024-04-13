from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import csv
import os

Constituency_list = []
opts = Options()
# Create a Firefox webdriver
driver = webdriver.Firefox(options=opts)

# Specify the CSV file name
csv_file_name = "election_results.csv"

if os.path.getsize(csv_file_name) != 0:
    print("File is Full")
    # Close the browser window
    driver.quit()
else:
    # Open a website
    url = 'https://results.eci.gov.in/ResultAcGenMay2023/ConstituencywiseS1046.htm?ac=46'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    draws = soup.find('select', id="ddlAC")
    for draw in draws.find_all('option'):
        Constituency_str = draw.text[-3:]
        if Constituency_str.isalpha():
            pass
        else:
            Constituency_list.append(Constituency_str)

    list_of_con = []

    for item in Constituency_list:
        if item[0] == '-':
            item.lstrip('-')
            list_of_con.append(int(item[1::]))
        elif item[0].isalpha():
            split_parts = item.split('-')
            # Extract only the integer part
            if len(split_parts) == 2 and split_parts[1].isdigit():
                integer_value = int(split_parts[1])
                list_of_con.append(integer_value)
        else:
            list_of_con.append(int(item))

    # Convert negative numbers to positive and add constituency list
    Con_list_url = ['https://results.eci.gov.in/ResultAcGenMay2023/ConstituencywiseS1034.htm?ac=' + str(abs(number)) for
                    number in list_of_con]
    count = 0
    # Header row data
    header_row = ['Constituency', 'Candidate', 'Party', 'EVM Votes', 'Postal Votes', 'Total Votes', '% of Votes']
    # Write data to CSV
    with open(csv_file_name, mode="w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row to the CSV
        writer.writerow(header_row)
        for url in Con_list_url:
            driver.get(url)
            soup1 = BeautifulSoup(driver.page_source, 'lxml')
            constituency_name = driver.find_element(By.XPATH, "//*[@id='div1']/table[1]/tbody/tr[1]/td")
            print("==========================================================")
            print(constituency_name.text[10::])
            print("==========================================================")
            # Find all rows in the table body
            rows = soup1.find('tbody').find_all('tr')[16:]
            # Extract and print the alignment attribute of each row and the content of each cell
            for row in rows:
                align_attribute = row.get('align')

                cells = row.find_all('td')
                cell_data = [cell.text for cell in cells]
                cell_data.insert(1, constituency_name.text[10::])
                # Break the loop when a cell contains 'Total'
                if any('Total' in cell for cell in cell_data):
                    break
                print(cell_data[1:])
                # Write the data as a single row
                writer.writerow(cell_data[1:])
            # break
        count += 1
    print("==========================================================")
    print(f"Total Constituency Count: {count}")
    print("==========================================================")
    time.sleep(4)

    # Close the browser window
    driver.quit()
