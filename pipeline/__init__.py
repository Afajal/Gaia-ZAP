from gaiasdk import sdk
import logging
import subprocess
import os
import git
from zapv2 import ZAPv2 as ZAP
import base64
import uuid
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import sys
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WeCareAuthScript(object):
    def __init__(self, proxy_host = 'localhost', proxy_port = '8090', target = 'http://localhost:9000'):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.target = target

    def run_script(self):
        options = Options()
        options.headless = True
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", 'localhost')
        profile.set_preference("network.proxy.http_port", 8090)
        profile.set_preference("network.proxy.ssl", 'localhost')
        profile.set_preference("network.proxy.ssl_port", 8090)
        profile.set_preference("network.proxy.no_proxies_on", "*.googleapis.com,*.google.com,*.gstatic.com,*.googleapis.com,*.mozilla.net,*.mozilla.com,ocsp.pki.goog")
        driver = webdriver.Firefox(firefox_profile=profile,options=options)
        logging.info("[+] Initialized firefox driver")
        driver.maximize_window()
        # logging.info("maximized window")
        driver.implicitly_wait(120)
        logging.info("[+] ================ Implicit Wait is Set =================")
        url = self.target
        driver.get('%s/login/' % url)
        logging.info('[+] ' + driver.current_url)
        time.sleep(10)
        driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').clear()
        driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').send_keys('bruce.banner@we45.com')
        driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').clear()
        driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').send_keys('secdevops')
        driver.find_element_by_xpath('/html/body/div/div/section/form/div[3]/button').click()
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.implicitly_wait(10)
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.implicitly_wait(10)
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/technicians/' % url)
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/appointment/plan' % url)
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/appointment/doctor' % url)
        time.sleep(10)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/secure_tests/' % url)
        time.sleep(10)
        # Sends keys and clicks on 'Search'
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
        driver.implicitly_wait(5)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/tests/' % url)
        time.sleep(10)
        # Sends keys and clicks on 'Search'
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
        driver.implicitly_wait(5)
        logging.info('[+] ' + driver.current_url)
        driver.get('%s/plans/' % url)
        time.sleep(10)

proxy_host = os.environ.get('ZAP_IP','localhost')
proxy_port = os.environ.get('ZAP_PORT',8090)
proxy_url = "http://{0}:{1}".format(proxy_host,proxy_port)
target_site = "http://{0}:9000".format(os.environ.get('TARGET_IP', 'localhost'))

def StartZAP(args):
    logging.info("ZAP Initiated")
    time.sleep(5)
    
    cmd = "/app/ZAP_2.7.0/zap.sh -daemon -host localhost -port 8090 -config api.disablekey=true -config 'api.addrs.addr.name=.*' -config api.addrs.addr.regex=true"
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    logging.info(stderr)

    logging.info('Target URL', target_site)
    zap = ZAP(proxies = {'http': proxy_url, 'https': proxy_url})
    policies = zap.ascan.scan_policy_names
    if 'Light' not in policies:
        light = zap.ascan.add_scan_policy('Light', alertthreshold='Low', attackstrength='Low')
        logging.info("[+] ================ Add Policy =================")
        logging.info('[+] Added Scan Policy')
    WeCareAuthScript(proxy_host=proxy_host, proxy_port=proxy_port, target=target_site).run_script()
    active_scan_id = zap.ascan.scan(target_site,scanpolicyname='Light')

    logging.info("==================================================")
    
def RunScript(args):
    logging.info("Started Application Walkthrough")

    WeCareAuthScript(proxy_host=proxy_host, proxy_port=proxy_port, target=target_site).run_script()

    logging.info("Application Walkthrough Finished!")
    logging.info("==================================================")

def RunActiveScan(args):
    logging.info("ZAP Active Scan Started!")
    time.sleep(5)

    active_scan_id = zap.ascan.scan(target_site,scanpolicyname='Light')

    logging.info("ZAP Active Scan Finished!")
    logging.info("==================================================")
    
def GenerateReport(args):
    logging.info("ZAP Scan Report")
    logging.info("[+] ================ Scan Completed =================")
    alerts = zap.core.alerts()
    logging.info('_'*125)
    logging.info('|'+' '*48+'Name'+' '*47+'  |'+'  Severity  '+'|'+'  CWE  |')
    logging.info('_'*125)
    for alert in alerts:
        name = alert.get('name')
        l = 100 - len(name)
        sev = alert.get('risk')
        sl = 10 - len(sev)
        cwe = alert.get('cweid')
        cl = 7 - len(cwe) - 1
        logging.info('| '+name+' '*l+'|  '+sev+' '*sl +'|  '+cwe+' '*cl+ '|')
        logging.info('_'*125)
    logging.info("==================================================")

def StopZAP(args):
    logging.info("ZAP tool shutting down started!")
    time.sleep(5)
    zap.core.shutdown()
    logging.info("ZAP tool shutting down finished!")
    logging.info("==================================================")
    
def main():
    logging.basicConfig(level=logging.INFO)
    startzap = sdk.Job("Start ZAP", "Starting ZAP", StartZAP)
    runscript = sdk.Job("Run Application Walkthrough", "Application Walkthrough Running", RunScript,["Start ZAP"])
    runactivescan = sdk.Job("Run ZAP Active Scan", "Running ZAP Scan", RunActiveScan, ["Run Application Walkthrough"])
    generatereport = sdk.Job("Generate ZAP Scan Report", "Generating ZAP Scan Report", GenerateReport, ["Run ZAP Active Scan"])
    stopzap = sdk.Job("Stop ZAP", "Stopping ZAP", StopZAP, ["Generate ZAP Scan Report"])
    sdk.serve([startzap, runscript, runactivescan, generatereport, stopzap])
