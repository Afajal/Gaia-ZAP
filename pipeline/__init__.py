from gaiasdk import sdk
import logging
import time
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
            logging.info("Spider running at {0}%".format(int(self.zap.spider.status(spider_id))))
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
            logging.info("Scan running at {0}%".format(int(self.zap.ascan.status(scan_id))))
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
        

proxy_host = os.environ.get('ZAP_IP','localhost')
proxy_port = os.environ.get('ZAP_PORT',8090)
proxy_url = "http://{0}:{1}".format(proxy_host,proxy_port)
target_site = os.environ.get('TARGET_URL','http://134.209.146.136')
zap = ZAP(proxies={
            "http": "http://{0}:{1}".format(self.proxy_host, self.proxy_port), 
            "https": "http://{0}:{1}".format(self.proxy_host, self.proxy_port)}
            )
context_id_list = []

def StartZAP(args):
    logging.info("ZAP Initiated")
    time.sleep(5)
    cmd = "/app/ZAP_2.7.0/zap.sh -daemon -host localhost -port 8090 -config api.disablekey=true -config 'api.addrs.addr.name=.*' -config api.addrs.addr.regex=true"
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    logging.info(stderr)
    time.sleep(20)
    
    regex = "{0}.*".format(target_site)
    context_id = self.zap.context.new_context(contextname="CTF2")
    time.sleep(1)
    zap.context.include_in_context(contextname, regex=regex)
    time.sleep(5)
    logging.info(context_id)
    context_id_list.append(context_id)
    logging.info(context_id_list)
    logging.info("CTF2 Context set successfully")
    
    logging.info("ZAP Started")
    logging.info("==================================================")
    
def RunScript(args):
    logging.info("Started Application Walkthrough")
    time.sleep(5)
    
    logging.info("Application Walkthrough Finished!")
    logging.info("==================================================")

def RunActiveScan(args):
    logging.info("ZAP Active Scan Started!")
    time.sleep(5)
    
    logging.info("ZAP Active Scan Finished!")
    logging.info("==================================================")
    
def GenerateReport(args):
    logging.info("ZAP Scan Report")
    time.sleep(5)
    logging.info("==================================================")

def StopZAP(args):
    logging.info("ZAP tool shutting down started!")
    zap.core.shutdown()
    time.sleep(5)
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
