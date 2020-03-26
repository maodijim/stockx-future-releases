import re
import smtplib
import argparse


def dict_to_string(dict_int):
    return_str = ""
    for item in dict_int.items():
        return_str += """{snk_name}
    Release Date: {release_date}
    Release Link: {link}
    Release Price: {release_price} 
    Premium: {premium}%
""".format(snk_name=item[0],
           release_date=" ".join(item[1]['release_date']),
           link=item[1]['release_href'],
           release_price=item[1]['retail_price'],
           premium=item[1]['price_prem'])
    return return_str


def send_email(smtp_server, email_user, email_password, send_from, send_to, msg,  smtp_port=587):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(send_from, send_to, email_msg_generator(send_from, send_to, msg))


def email_msg_generator(send_from, send_to, msg):
    email_msg = """\
From:{send_from}
To:{send_to}
Subject: Upcoming releases

{msg}
""".format(send_from=send_from, send_to=send_to, msg=msg)
    return email_msg


def get_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", help="Email that will receive notification")
    parser.add_argument("--driver-path", help="path to chrome driver path")
    args = parser.parse_args()

    if not args.driver_path:
        args.driver_path = input("Please Enter Firefox Webdriver path: ")

    return args


def price_extrator(content):
    """
    Extrat price from a string
    :param content: string contains price tag
    :return: float price
    """
    price_regex = re.compile("\$?[0-9.]+")
    price = 0.0
    if re.search(price_regex, content):
        price = float(re.search(price_regex, content).group(0).replace("$", ""))
    else:
        print("No price found")
    return price


def percentage_extrator(content_list):
    """
    :param content_list: list of gauge-value from stockx
    :return: float Price Premium percentage
    """
    percentage = 0.0
    for content in content_list:
        if re.match("[0-9.]+%", content.text):
            percentage = float(content.text.replace('%', ''))
    return percentage
