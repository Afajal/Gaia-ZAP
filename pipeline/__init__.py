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

def StartZAP(args):
            logging.info("ZAP Initiated")
            time.sleep(5)
            
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
