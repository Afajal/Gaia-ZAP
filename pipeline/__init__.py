from gaiasdk import sdk
import logging
import time
import subprocess
import os
import git
from OwaspZAP import *

def StartZAP(args):
    logging.info("ZAP Initiated")
    time.sleep(5)
    
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

    
def main():
    logging.basicConfig(level=logging.INFO)
    startzap = sdk.Job("Start ZAP", "Starting ZAP", StartZAP)
    runscript = sdk.Job("Run Application Walkthrough", "Application Walkthrough Running", RunScript,["Start ZAP"])
    runactivescan = sdk.Job("Run ZAP Active Scan", "Running ZAP Scan", RunActiveScan, ["Run Application Walkthrough"])
    generatereport = sdk.Job("Generate ZAP Scan Report", "Generating ZAP Scan Report", GenerateReport, ["Run ZAP Active Scan"])
    sdk.serve([startzap, runscript, runactivescan, generatereport])
