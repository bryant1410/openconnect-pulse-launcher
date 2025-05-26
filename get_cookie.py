#!/usr/bin/env python

import getopt
import logging
import os
import shutil
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from xdg_base_dirs import xdg_config_home


def get_cookie(vpn_url: str, chromedriver_path: str, chromium_path: str) -> str:
    chrome_profile_dir = os.path.join(xdg_config_home(), "chromedriver", "pulsevpn")
    if not os.path.exists(chrome_profile_dir):
        os.makedirs(chrome_profile_dir)

    dsid = None

    while True:
        if not dsid or "value" not in dsid:
            service = Service(executable_path=chromedriver_path)
            options = webdriver.ChromeOptions()
            options.binary_location = chromium_path
            options.add_argument("--window-size=800,900")
            options.add_argument("user-data-dir=" + chrome_profile_dir)

            logging.info("Starting browser.")
            driver = webdriver.Chrome(service=service, options=options)

            driver.get(vpn_url)
            dsid = WebDriverWait(driver, float("inf")).until(lambda driver: driver.get_cookie("DSID"))
            driver.quit()
            return dsid["value"]

def main() -> None:
    argv = sys.argv[1:]

    chromedriver_path = shutil.which("chromedriver")
    chromium_path = shutil.which("chromium") or shutil.which("google-chrome")
    help_message = f"{os.path.basename(__file__)} <vpn_url>".format()

    try:
        opts, args = getopt.getopt(argv, "hds:c:", ["help", "chromedriver-path"])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    if len(args) != 1:
        print(help_message)
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print(help_message)
            sys.exit()
        elif o in ("-c", "--chromedriver-path"):
            if len(a):
                chromedriver_path = a
    vpn_url = args[0]

    print(get_cookie(vpn_url, chromedriver_path=chromedriver_path, chromium_path=chromium_path))


if __name__ == "__main__":
    main()
