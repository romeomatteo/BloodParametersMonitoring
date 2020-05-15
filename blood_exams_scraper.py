from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pathlib2 import Path
import time
import os
import json
from datetime import datetime


class BloodScraper():

    def __init__(self):
        return


def main():
    return


def wait_clickable_and_click_by_id(browser, id):
    el = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, id)))
    el.click()


def wait_selected_and_click_by_id(browser, id):
    el = WebDriverWait(browser, 10).until(
        EC.element_to_be_selected((By.ID, id)))
    el.click()


def download_exam(browser, date, download_path, referti_path):
    exam_el = browser.find_element_by_xpath(
        "//ul[@id='esamiListViewEsami']//li//a//label[text()='{}']".format(date))
    print(exam_el)
    time.sleep(2)
    exam_el.click()
    print('clicked')
    #
    data = browser.find_element_by_id('esameUltimoEsameDataEsecuzione').text
    link_doc_referto_raw = browser.find_element_by_xpath(
        "//a[contains(text(), 'RefertoOriginale.pdf')]")
    link_doc_referto_raw.click()

    time.sleep(2)

    link_doc_refertoAVIS = browser.find_element_by_xpath(
        "//a[contains(text(), 'RefertoAVIS.pdf')]")
    link_doc_refertoAVIS.click()
    # elementi_esame = browser.find_elements_by_xpath("//ul[@id='esamiListViewEsami']//li")
    time.sleep(2)
    data = datetime.strptime(data, '%d/%m/%Y').strftime(format='%Y%m%d')
    print(data)
    raw_name = 'referto_raw_{}.pdf'.format(data)
    avis_name = 'referto_AVIS_{}.pdf'.format(data)
    referto_path = referti_path / data
    if not os.path.exists(referto_path):
        referto_path.mkdir()

    for file in download_path.glob('*.pdf'):
        if '(1)' not in file.stem:
            file.rename(referto_path / raw_name)
        elif '(1)' in file.stem:
            file.rename(referto_path / avis_name)

    browser.back()


if __name__ == '__main__':
    referti_path = Path("Referti")
    download_path = Path(__file__).cwd() / 'temppdfdownloads'
    config_file = Path('config.json')

    with open(config_file.name) as data_file:
        params = json.load(data_file)

    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_path.as_posix())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf')
    # disable Firefox's built-in PDF viewer
    profile.set_preference("pdfjs.disabled", True)

    # disable Adobe Acrobat PDF preview plugin
    profile.set_preference("plugin.scan.plid.all", False)
    profile.set_preference("plugin.scan.Acrobat", "99.0")

    browser = webdriver.Firefox(executable_path=params['gekoexecutable'],
                                firefox_profile=profile)
    print('Open')
    browser.get(params['avis_address'])
    print('Open end')
    try:
        print('Straiting wait')
        browser.implicitly_wait(10)
        iframe = browser.find_element_by_id('blockrandom')
        browser.get(iframe.get_attribute('src'))
        print('Switched to iframe')

        wait_clickable_and_click_by_id(browser=browser, id="loginDonatore")
        username_text = browser.find_element_by_id('registrazioneRichiediPINEMail')
        username_text.send_keys(params['username'])
        PIN_text = browser.find_element_by_id('registrazioneRichiediPINInserisci')
        PIN_text.send_keys(params['password'])
        browser.find_element_by_id('registrazioneRichiediPINConcludi').click()

        wait_clickable_and_click_by_id(browser=browser, id="esitiEsamiMenuItem")

        time.sleep(3)
        wait_clickable_and_click_by_id(browser=browser, id="esameTutte")

        time.sleep(3)
        # browser.find_element_by_id('esitiEsamiMenuItem').click()
        # browser.find_element_by_id('esameTutte').click()
        exam_dates = [a.text for a in
                      browser.find_elements_by_xpath(
                          "//ul[@id='esamiListViewEsami']//li//a//label[@class='data']")][::2]

        for d in exam_dates:
            download_exam(browser=browser, date=d, download_path=download_path, referti_path=referti_path)
            print('downloading only last exam')
            break
        browser.close()

    except Exception as e:
        print(e)

    # browser.find_element_by_id(id_='loginDonatore').click()
