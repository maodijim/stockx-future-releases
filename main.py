import utilities
import traceback
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Global Variables
email_server = ""
email_user = ""
email_pass = ""
send_to_email = []


#############################################
prem_percent = 45
stockx_url = "https://stockx.com/new-releases/sneakers"

def load_releases(driver, url):
    """
    load future sneakers release from https://stockx.com/new-releases/sneakers
    :param driver: selenium chrome driver
    :param url: stockx release page url
    :return: list of future releases
    """
    driver.get(url)
    return driver.find_elements_by_class_name("release-tile")


def select_releases(driver, releases_list, targeted_price=200.0):
    """
    filter our releases that meet the targeted price
    :param driver: selenium chrome driver
    :param releases_list: list of releases contains all
    :param targeted_price: float filter out sneakers cheaper than targeted price
    :return: dict {"release_href": url str, "release_date": []}
    """
    selected_releases = {}
    for release in releases_list:
        release_name = release.find_element_by_tag_name('a').get_attribute('id')
        release_href = release.find_element_by_tag_name('a').get_attribute('href')
        release_date = release.find_element_by_class_name('release-month').text.split("|")
        release_date = list(map(str.strip, release_date))
        try:
            driver.implicitly_wait(0)
            release_bid = utilities.price_extrator(release.find_element_by_class_name('highest-bid').text)
            driver.implicitly_wait(20)
        except NoSuchElementException:
            release_bid = 0.0
        if release_bid > targeted_price:
            selected_releases[release_name] = {"release_href": release_href, "release_date": release_date}
    return selected_releases


def find_profit_snk(driver, selected_sneakers, prem=50):
    profit_dict = selected_sneakers.copy()
    for sneaker in selected_sneakers.items():
        driver.get(sneaker[1]['release_href'])
        price_prem = utilities.percentage_extrator(driver.find_elements_by_class_name("gauge-value"))
        if price_prem < prem:
            del profit_dict[sneaker[0]]
        else:
            retail_price = driver.find_element_by_xpath("//span[@class='title' and text()='Retail Price']//following::span[1]").text
            profit_dict[sneaker[0]]['retail_price'] = retail_price
            profit_dict[sneaker[0]]['price_prem'] = price_prem
    return profit_dict


def main():
    releases = load_releases(browser_driver, stockx_url)
    final_releases_list = find_profit_snk(browser_driver, select_releases(browser_driver, releases), prem=prem_percent)
    if len(final_releases_list) > 0:
        for email in send_to_email:
            try:
                utilities.send_email(smtp_server=email_server,
                                     email_user=email_user,
                                     email_password=email_pass,
                                     send_from=email_user,
                                     send_to=email,
                                     msg=utilities.dict_to_string(final_releases_list))
            except:
                traceback.print_exc()
                print("Failed to send email to %s" % email)
    print(utilities.dict_to_string(final_releases_list))


if __name__ == '__main__':
    args = utilities.get_args()
    browser_driver = webdriver.Firefox(executable_path=args.driver_path)
    browser_driver.set_window_size(1024, 768)
    browser_driver.implicitly_wait(20)
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        browser_driver.close()
