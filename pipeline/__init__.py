from zapv2 import ZAPv2 as ZAP
import time
import subprocess
import base64
import uuid
import json
import requests
from datetime import datetime
from gaiasdk import sdk
import logging
import os
import git
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import sys
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class OwaspZAP(object):
    def __init__(self, proxy_host='localhost', proxy_port='8090'):
        logging.info('in class')
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.zap = ZAP(proxies={
            "http": "http://{0}:{1}".format(self.proxy_host, self.proxy_port), 
            "https": "http://{0}:{1}".format(self.proxy_host, self.proxy_port)}
            )

    def start_headless_zap(self, zap_path, proxy_port):
        try:
            cmd = "{0}/zap.sh -daemon -config api.disablekey=true -port {1}".format(zap_path, proxy_port)
            logging.info(cmd)
            subprocess.Popen(cmd.split(" "), stdout=open(os.devnull, "w"))
            time.sleep(10)
        except IOError:
            logging.info("ZAP Path is not configured correctly")

    def zap_open_url(self, url):
        self.zap.urlopen(url)
        time.sleep(4)

    def zap_define_context(self, contextname, url):
        regex = "{0}.*".format(url)
        context_id = self.zap.context.new_context(contextname=contextname)
        time.sleep(1)
        self.zap.context.include_in_context(contextname, regex=regex)
        time.sleep(5)
        return context_id

    def zap_start_spider(self, contextname, url):
        try:
            spider_id = self.zap.spider.scan(url=url, contextname=contextname)
            time.sleep(2)
            return spider_id
        except Exception as e:
            logging.info((e.message))

    def zap_spider_status(self, spider_id):
        while int(self.zap.spider.status(spider_id)) < 100:
            print("Spider running at {0}%".format(int(self.zap.spider.status(spider_id))))
            time.sleep(10)
        logging.info("Spider Completed!")
        logging.info(self.zap.core.urls())

    def zap_start_ascan(self, context, url, policy="Default Policy"):
        try:
            scan_id = self.zap.ascan.scan(contextid=context, url=url, scanpolicyname=policy)
            time.sleep(2)
            return scan_id
        except Exception as e:
            logging.info(e.message)

    def zap_scan_status(self, scan_id):
        while int(self.zap.ascan.status(scan_id)) < 100:
            print("Scan running at {0}%".format(int(self.zap.ascan.status(scan_id))))
            time.sleep(10)
        logging.info('Active Scan Complete!')
        logging.info(self.zap.core.alerts())

    def zap_export_html_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.htmlreport())
        f1.close()
        logging.info("HTML REPORT GENERATED")
    
    def zap_export_xml_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.xmlreport())
        f1.close()
        logging.info("XML REPORT GENERATED")
        
    def zap_export_json_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.jsonreport())
        f1.close()
        logging.info("JSON REPORT GENERATED")

    def zap_shutdown(self):
        self.zap.core.shutdown()

class CTF2_walkthrough(object):
	def __init__(self, proxy_host = 'localhost', proxy_port = '8090',target= os.environ.get('TARGET_URL','http://134.209.146.136')):
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
		profile.accept_untrusted_certs = True
		profile.DEFAULT_PREFERENCES["frozen"]["marionette.contentListener"] = True
		profile.DEFAULT_PREFERENCES["frozen"]["network.stricttransportsecurity.preloadlist"] = True
		profile.DEFAULT_PREFERENCES["frozen"]["security.cert_pinning.enforcement_level"] = True
		profile.set_preference('webdriver_assume_untrusted_issuer',False)
		desired_capabilities = DesiredCapabilities.FIREFOX.copy()
		desired_capabilities['acceptInsecureCerts'] = True
		profile.set_preference("network.proxy.no_proxies_on", "*.googleapis.com,*.google.com,*.gstatic.com,*.googleapis.com,*.mozilla.net,*.mozilla.com,ocsp.pki.goog")
		driver = webdriver.Firefox(firefox_profile=profile,firefox_options=options,capabilities=desired_capabilities)	
		print("[+] Initialized firefox driver")
		driver.maximize_window()
		driver.implicitly_wait(10)
		print("[+] ================ Implicit Wait is Set =================")
		driver.get('{0}'.format(target))
        	print('[+] ' + driver.current_url)
        	driver.implicitly_wait(5)
        	# Clicks on 'About'
		try:
		    driver.get('{0}/about'.format(target))
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/appointment/add'.format(target))
		    logging.info('[+] ' + driver.current_url)
		    driver.implicitly_wait(5)
		    time.sleep(10)
		    # Name
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[1]/div/div/input').clear()
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[1]/div/div/input').send_keys('selenium test')
		    driver.implicitly_wait(5)
		    # Phone number
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[1]/div/div/input').clear()
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[1]/div/div/input').send_keys('0011223344')
		    driver.implicitly_wait(5)
		    # Gender
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[1]/div/div/select').click()
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[1]/div/div/select/option[2]').click()
		    driver.implicitly_wait(5)
		    # Health Plan
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select').click()
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select/option[3]').click()
		    driver.implicitly_wait(5)
		    # Select Health Plan
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select').click()
		    driver.implicitly_wait(10)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select/option[2]').click()
		    driver.implicitly_wait(7)
		    # Appointment reason
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').send_keys('Selenium Test')
		    # Email
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').send_keys('selenium@test.com')
		    driver.implicitly_wait(5)
		    # Date of Birth
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').send_keys('1989-01-04')
		    driver.implicitly_wait(5)
		    # Address
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').send_keys('Selenium Test')
		    driver.implicitly_wait(5)
		    # Appointment Date
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').send_keys('2021/01/04')
		    driver.implicitly_wait(5)
		    # Submit
		    driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[7]/div/div/input').click()
		    driver.implicitly_wait(5)
		    time.sleep(10)
		    driver.get('{0}/contact_us/'.format(target))
		    logging.info( '[+] ' + driver.current_url)
		    time.sleep(10)
		except BaseException as e:
		    pass

		try:
		    driver.get('{0}/login/'.format(target))
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
		    driver.get('{0}/technicians/'.format(target))
		    time.sleep(10)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/appointment/plan'.format(target))
		    time.sleep(10)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/appointment/doctor'.format(target))
		    time.sleep(10)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/secure_tests/'.format(target))
		    time.sleep(10)
		    # Sends keys and clicks on 'Search'
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
		    driver.implicitly_wait(5)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/tests/'.format(target))
		    time.sleep(10)
		    # Sends keys and clicks on 'Search'
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
		    driver.implicitly_wait(5)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/plans/'.format(target))
		    time.sleep(10)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/password_change'.format(target))
		    time.sleep(10)
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
		    driver.implicitly_wait(5)
		    logging.info('[+] ' + driver.current_url)
		    driver.get('{0}/password_change_secure'.format(target))
		    time.sleep(10)
		    driver.implicitly_wait(5)
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
		    driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
		    driver.implicitly_wait(5)
		    logging.info('[+] ' + driver.current_url)
		except BaseException as e:
		    logging.info(e)
        
proxy_host = os.environ.get('ZAP_IP','localhost')
proxy_port = os.environ.get('ZAP_PORT',8090)
proxy_url = "http://{0}:{1}".format(proxy_host,proxy_port)
target_site = os.environ.get('TARGET_URL','http://134.209.146.136')
context_id_list = []
owasp_zap = OwaspZAP(proxy_host=proxy_host, proxy_port=proxy_port)

def StartZAP(args):
    logging.info("ZAP tool initialization started!")
    owasp_zap.start_headless_zap(zap_path='/app/ZAP_2.7.0', proxy_port=proxy_port)
    time.sleep(20)
    owasp_zap.zap_open_url(url=target_site)
    context_id = owasp_zap.zap_define_context(contextname='CTF2', url=target_site)
    context_id_list.append(context_id)
    logging.info("ZAP tool initialization finished!")
    logging.info("==================================================")
    
def StartProxy(args):
    logging.info("ZAP Proxy has been started!")
    time.sleep(10)
    logging.info("ZAP Proxy has been finished!")
    logging.info("==================================================")

def RunWalkthrough(args):
    logging.info("Walkthrough of Application has been started!")
    CTF2_walkthrough(proxy_host=proxy_host, proxy_port=proxy_port, target=target_site).run_script()
    time.sleep(5)
    logging.info("Walkthrough of Application has been finished!")
    logging.info("==================================================")
 
def RunSpiderScan(args):
    logging.info("ZAP Spider Scan has been started!")
    spider_id = owasp_zap.zap_start_spider(contextname='CTF2', url=target_site)
    owasp_zap.zap_spider_status(spider_id=spider_id)
    time.sleep(5)
    logging.info("ZAP Spider Scan has been finished!")
    logging.info("==================================================")

def RunActiveScan(args):
    logging.info("ZAP Scan has been started!")
    scan_id = owasp_zap.zap_start_ascan(context=context_id_list[0], url=target_site)
    owasp_zap.zap_scan_status(scan_id=scan_id)
    time.sleep(5)
    logging.info("ZAP Scan has been finished!")
    logging.info("==================================================")
    
def GenerateReport(args):
    logging.info("ZAP Scan report generation has been started!")
    owasp_zap.zap_export_json_report(export_file='parameterized_ctf2_zap_scan.json')
    time.sleep(5)
    logging.info("ZAP Scan report generation been finished!")
    logging.info("==================================================")

def StopZAP(args):
    logging.info("ZAP tool shutting down started!")
    owasp_zap.zap_shutdown()
    time.sleep(5)
    logging.info("ZAP tool shutting down finished!")
    logging.info("==================================================")

def main():
    logging.basicConfig(level=logging.INFO)
    startzap = sdk.Job("Start ZAP", "Starting ZAP", StartZAP)
    startproxy = sdk.Job("Start Proxy", "Starting Proxy", StartProxy,["Start ZAP"])
    runwalkthrough = sdk.Job("Run Walkthrough", "Starting Walkthrough", RunWalkthrough,["Start Proxy"])
    runspiderscan = sdk.Job("Run Spider Scan", "Starting ZAP Spider Scan", RunSpiderScan,["Run Walkthrough"])
    runactivescan = sdk.Job("Run Active Scan", "Starting ZAP Active Scan", RunActiveScan,["Run Spider Scan"])
    generatereport = sdk.Job("Generate Report", "GenerateReporting ZAP Scan Report", RunScan,["Run Acitve Scan"])
    stopzap = sdk.Job("Stop ZAP", "Stopping ZAP", RunScan,["Generate Report"])
    sdk.serve([startzap, startproxy, runwalkthrough, runspiderscan, runactivescan, generatereport, stopzap])
