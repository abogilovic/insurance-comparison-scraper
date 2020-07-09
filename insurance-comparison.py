import os
import time
from datetime import datetime
import pandas as pd
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

V_DISP = False
LOAD_IMGS = False
MAKE_CSV_FROM_LIST = False
MAKE_CSV_FROM_DATA_FRAME = True
CLOSE = True

def setup_chrome_webdriver(path="/home/gillabo/Desktop/upwork/chromedriver",
                           virtual_display=False, load_imgs=False, maximized=True, headless=False):
    display = None
    if virtual_display:
        display = Display(visible=0, size=(1920, 1080))
        display.start()

    chrome_options = webdriver.ChromeOptions()
    if not load_imgs:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("no-sandbox")
    if maximized: chrome_options.add_argument("start-maximized")
    if headless: chrome_options.add_argument("headless")

    start_time = datetime.now().strftime("%H:%M:%S")
    print("Start time: {}".format(start_time))
    return [webdriver.Chrome(executable_path=path, chrome_options=chrome_options), display, start_time]

def close_webdriver(driver, display, start_time):
    current_time = datetime.now().strftime("%H:%M:%S")
    print("Start time: {} \nEnd time: {}".format(start_time, current_time))
    driver.quit()
    if display: display.stop()

def make_csv_from_list(data, name, columns, sep=',', drop_duplicates=True):
    df = pd.DataFrame(data, columns=columns)
    if drop_duplicates: df = df.drop_duplicates()
    df.to_csv("{}/{}.csv".format(os.path.dirname(os.path.realpath(__file__)), name), sep=sep, index=False)

def make_csv_form_data_frame(df, name, sep=',', drop_duplicates=True):
    if drop_duplicates: df = df.drop_duplicates()
    df.to_csv("{}/{}.csv".format(os.path.dirname(os.path.realpath(__file__)), name), sep=sep, index=False)

def selenium_scraping():
    # driver and display initialisation
    setup_data = setup_chrome_webdriver(virtual_display=V_DISP, load_imgs=LOAD_IMGS)
    driver = setup_data[0];
    display = setup_data[1];
    start_time = setup_data[2]
    animation = ["[#.........]", "[##........]", "[###.......]", "[####......]", "[#####.....]", "[######....]",
                 "[#######...]", "[########..]", "[#########.]", "[##########]"]

    # custom behaviour
    data = custom_behaviour(driver)

    # make csv
    if MAKE_CSV_FROM_LIST: make_csv_from_list(data, 'output', [], sep=',', drop_duplicates=True)
    elif MAKE_CSV_FROM_DATA_FRAME: make_csv_form_data_frame(data, "output_data", sep=';', drop_duplicates=False)

    # quit
    if CLOSE: close_webdriver(driver, display, start_time)
    else: input()


def custom_behaviour(driver):
    df = pd.read_csv('./input_data_example.csv', sep=';')
    if 'car_price_quote_dict' not in df.columns:
        df['car_price_quote_dict'] = ""

    configuration_id = df.iloc[:,0]
    car_brand = df['car_brand']; car_model = df['car_model']; car_year = df['car_year']; car_motor_size = df['car_motor_size']
    car_variation = df['car_variation']; insurance_config_kilometers = df['insurance_config_kilometers']
    insurance_config_deductible = df['insurance_config_deductible']; insurance_config_allrisk = df['insurance_config_allrisk']
    insurance_config_freeclaim = df['insurance_config_freeclaim']; insurance_config_ext_glass = df['insurance_config_ext_glass']
    insurance_config_driver_cov = df['insurance_config_driver_cov']; insurance_config_road_assistance = df['insurance_config_road_assistance']
    insurance_config_is_leasing = df['insurance_config_is_leasing']; risk_profile_age = df['risk_profile_age']
    risk_profile_address = df['risk_profile_address']; risk_profile_years_own_car_insurance = df['risk_profile_years_own_car_insurance']
    risk_profile_claims_past_5_years = df['risk_profile_claims_past_5_years']
    risk_profile_first_claim_year = df['risk_profile_first_claim_year']; risk_profile_second_claim_year = df['risk_profile_second_claim_year']
    risk_profile_third_claim_year = df['risk_profile_third_claim_year']

    driver.get('https://forsikringsguiden.dk/')

    current_time = datetime.now().strftime("%H:%M:%S")
    print("Start time: {}".format(current_time))

    # ENTERING STAGE
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'button.primary.inverse'))).click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'car'))).click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'button.primary.arrow-right.ng-star-inserted'))).click()

    for i in range(len(configuration_id)):
        # STAGE 1
        el_risk_profile_address = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'autoInput')))
        el_risk_profile_age = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'customerAge')))
        el_risk_profile_address.clear()
        el_risk_profile_address.send_keys(risk_profile_address[i], Keys.TAB)
        el_risk_profile_age.clear()
        el_risk_profile_age.send_keys(str(risk_profile_age[i]), Keys.ENTER)
        len_warn = 0
        while len_warn!=2:
            time.sleep(0.1)
            warn = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'warn.hidden')))
            len_warn = len(warn)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[2]/app-common/section/div/div/fieldset/div[2]/div/div[2]/div/button'))).click()

        # STAGE 2
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'link-color-alternate'))).click()
        veh_cfg_len = 0
        vehicle_config = None
        while veh_cfg_len<5:
            time.sleep(0.1)
            vehicle_config = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.NAME, 'autoInput')))
            veh_cfg_len = len(vehicle_config)
        while not vehicle_config[0].is_enabled(): time.sleep(0.1)
        keys = car_brand[i]
        vehicle_config[0].send_keys(keys)
        for li in driver.find_element_by_class_name('suggestions.ng-star-inserted').find_elements_by_tag_name('li'):
            if li.text.strip()==keys:
                li.click(); break
        while not vehicle_config[1].is_enabled(): time.sleep(0.1)
        keys = car_model[i]
        vehicle_config[1].send_keys(keys)
        for li in driver.find_element_by_class_name('suggestions.ng-star-inserted').find_elements_by_tag_name('li'):
            if li.text.strip()==keys:
                li.click(); break
        while not vehicle_config[2].is_enabled(): time.sleep(0.1)
        keys = str(car_year[i])
        vehicle_config[2].send_keys(keys)
        for li in driver.find_element_by_class_name('suggestions.ng-star-inserted').find_elements_by_tag_name('li'):
            if li.text.strip() == keys:
                li.click(); break
        while not vehicle_config[3].is_enabled(): time.sleep(0.1)
        keys = car_motor_size[i]
        vehicle_config[3].send_keys(keys)
        for li in driver.find_element_by_class_name('suggestions.ng-star-inserted').find_elements_by_tag_name('li'):
            if li.text.strip() == keys:
                li.click(); break
        while not vehicle_config[4].is_enabled(): time.sleep(0.1)
        keys = car_variation[i]
        vehicle_config[4].send_keys(keys)
        for li in driver.find_element_by_class_name('suggestions.ng-star-inserted').find_elements_by_tag_name('li'):
            if li.text.strip() == keys:
                li.click(); break

        driver.find_element_by_id('insuredyears').send_keys(str(risk_profile_years_own_car_insurance[i]))
        val_risk_profile_claims_past_5_years = int(risk_profile_claims_past_5_years[i])
        if val_risk_profile_claims_past_5_years>0:
            insurance_claims = driver.find_element_by_name('insuranceClaims')
            insurance_claims.click()
            if val_risk_profile_claims_past_5_years>10: val_risk_profile_claims_past_5_years = 10
            kolone_profile_claims = [risk_profile_first_claim_year[i], risk_profile_second_claim_year[i], risk_profile_third_claim_year[i]]
            claim_years = []
            if val_risk_profile_claims_past_5_years>3: val_risk_profile_claims_past_5_years = 3
            for kol in kolone_profile_claims:
                if kol<2015: val_risk_profile_claims_past_5_years-=1
            for s in range(val_risk_profile_claims_past_5_years): insurance_claims.send_keys(Keys.ARROW_DOWN)
            insurance_claims.send_keys(Keys.ENTER)
            time.sleep(0.1)
            for y in range(val_risk_profile_claims_past_5_years):
                claim_years.append(driver.find_element_by_name('claim{}Year'.format(y+1)))
            for c in range(len(claim_years)):
                claim_year = claim_years[c]
                claim_year.click()
                n_down = 2020 - (int(kolone_profile_claims[c])-1) if 2020 - (int(kolone_profile_claims[c])-1) <= 6 else 6 #ASK neki su ispod 2015 a to je min
                for n in range(n_down): claim_year.send_keys(Keys.ARROW_DOWN)
                claim_year.send_keys(Keys.ENTER)
        driver.find_element_by_class_name('button.primary.arrow-right.ng-star-inserted').click()

        # STAGE 3
        spinner = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'container-spinner')))
        WebDriverWait(driver, 30).until(EC.staleness_of(spinner))
        driver.find_element_by_class_name('adjust-coverage').click()
        sliders = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'mat-slider-thumb')))
        full_w = driver.find_element_by_class_name('mat-slider-track-wrapper').size['width']
        move = ActionChains(driver)
        x_offset = (int((int(insurance_config_kilometers[i])/1000)-15) - 1) * full_w/59
        move.click_and_hold(sliders[0]).move_by_offset(x_offset, 0).release().perform()
        x_offset = (int((int(insurance_config_deductible[i])/1000) - 5)) * full_w / 20
        move = ActionChains(driver)
        move.click_and_hold(sliders[1]).move_by_offset(x_offset, 0).release().perform()

        boolean_adjustments = driver.find_element_by_class_name('grid-x.margin-top-small')
        if not insurance_config_allrisk[i]: #insurance_config_allrisk # NEGATION
            boolean_adjustments.find_element_by_xpath('.//div[1]/div[2]/div/label/span').click()
        else:
            if insurance_config_freeclaim[i]: #insurance_config_free_claim
                boolean_adjustments.find_element_by_xpath('.//div[2]/div[2]/div/label/span').click()
            if insurance_config_ext_glass[i]: #insurance_config_ext_glass
                boolean_adjustments.find_element_by_xpath('.//div[2]/div[3]/div/label/span').click()
        if insurance_config_driver_cov[i]: #insurance_config_driver_cov
            boolean_adjustments.find_element_by_xpath('.//div[1]/div[3]/div/label/span').click()
        if insurance_config_road_assistance[i]: #insurance_config_road_assistance
            boolean_adjustments.find_element_by_xpath('.//div[1]/div[4]/div/label/span').click()
        if insurance_config_is_leasing[i]: #insurance_config_is_leasing
            v = 3 if insurance_config_allrisk[i] else 2 #insurance_config_allrisk
            boolean_adjustments.find_element_by_xpath('.//div[{}]/div[3]/div/label/span'.format(v)).click()
        driver.find_element_by_xpath('//*[@id="refiner-popup"]/div[1]/div/app-result-popup/section/div/div/div[2]/div[2]/div[3]/div[2]/div/button[2]').click()

        # STAGE 4
        spinner = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'container-spinner')))
        WebDriverWait(driver, 30).until(EC.staleness_of(spinner))

        car_price_quote_dict_list = []
        matches = driver.find_element_by_class_name('container-matches').find_elements_by_xpath('.//app-offer-match')

        for k in range(len(matches)):
            car_price_quote_dict = {}
            match = matches[k]
            match.find_element_by_class_name('button.mini-accordion').click()
            match.find_element_by_class_name('container-insurance-list').click()

            c_1 = match.find_element_by_xpath('.//div[1]/div[1]/img').get_attribute('src')
            print(c_1)
            c_2 = float(match.find_element_by_xpath('.//div[2]/div[2]/div/div[1]/div[3]/div/div[1]').text.split(' ')[-1].replace('.',''))
            print(c_2)
            c_3 = float(match.find_element_by_xpath('.//div[3]/div/div[2]/div/div[1]/span[2]').text.replace('.',''))
            c_4 = float(match.find_element_by_xpath('.//div[3]/div/div[2]/div/div[3]/span[2]').text.replace('.',''))

            c_5 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]').get_attribute('class') == 'icon-text'
            c_6 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[3]/div/div[2]').get_attribute('class') == 'icon-text'
            c_7 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[5]/div/div[2]').get_attribute('class') == 'icon-text'
            c_8 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[7]/div/div[2]').get_attribute('class') == 'icon-text'
            c_9 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[9]/div/div[2]').get_attribute('class') == 'icon-text'

            c_10 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]').get_attribute('class') == 'icon-text'
            c_11 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[4]/div/div[2]').get_attribute('class') == 'icon-text'
            c_12 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[6]/div/div[2]').get_attribute('class') == 'icon-text'
            c_13 = match.find_element_by_xpath('.//div[2]/div[2]/div/div[2]/div[2]/div[8]/div/div[2]').get_attribute('class') == 'icon-text'
            c_14 = k+1


            car_price_quote_dict["company_image"] = c_1
            car_price_quote_dict["deductible"] = c_2
            car_price_quote_dict["total_price"] = c_3
            car_price_quote_dict["discounted_price"] = c_4
            car_price_quote_dict["configuration_result"] = {"is_allrisk": c_5,
                                                            "is_ext_glass": c_6,
                                                            "is_road_assistance": c_7,
                                                            "is_parking": c_8,
                                                            "is_young_driver": c_9,
                                                            "is_free_claim": c_10,
                                                            "is_driver_cov": c_11,
                                                            "is_fixed_price": c_12,
                                                            "is_leasing": c_13}
            car_price_quote_dict["rank"] = c_14
            car_price_quote_dict["configuration_id"] = configuration_id[i]
            car_price_quote_dict_list.append(car_price_quote_dict)

        df.at[i, 'car_price_quote_dict'] = car_price_quote_dict_list
        driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/app-result/section/div/div/div[1]/div[1]/div[1]').click()

    if 'Unnamed: 0' in df.columns: df.rename(columns={'Unnamed: 0': ''}, inplace=True)
    return df

if __name__=='__main__':
    selenium_scraping()
