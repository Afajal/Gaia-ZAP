from gaiasdk import sdk
import logging
import time
import subprocess
import os
import git

path_parent = os.getcwd()

nodejs_path = path_parent+"/Cut-The-Funds-NodeJS"
npm_audit_path = path_parent+"/Cut-The-Funds-NodeJS"

def Clone(args):
    logging.info("Cloning Latest Source started!")
    time.sleep(5)
    
    cmd = "rm -rf {0} | true".format(nodejs_path)
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    logging.info(stderr)
    logging.info("Cleared previous source code")
    
    git.Repo.clone_from('https://github.com/we45/Cut-The-Funds-NodeJS.git', 'Cut-The-Funds-NodeJS')
    logging.info("Cloning Latest Source finished!")
    
def RunNodejsScan(args):
    logging.info("NodejsScan has been started!")
    cmd = "nodejsscan -d {0}".format(nodejs_path)
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    logging.info(stderr)
    logging.info("NodejsScan has been finished!")
    logging.info("==================================================")

def RunNpmAudit(args):
    logging.info("NpmAudit has been started!")
    cmd = "npm audit --prefix {0}".format(npm_audit_path)
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
    stdout, stderr = process.communicate()
    logging.info(stdout)
    logging.info(stderr)
    logging.info("NpmAudit has been finished!")
    logging.info("==================================================")

    
def main():
    logging.basicConfig(level=logging.INFO)
    clone = sdk.Job("Clone Source", "Cloning Latest Source", Clone)
    runnodejsscan = sdk.Job("Run NodeJS Scan", "Running Bandit Scan", RunNodejsScan,["Clone Source"])
    runnpm = sdk.Job("Run Npm Audit Scan", "Running Safety Scan", RunNpmAudit, ["Run NodeJS Scan"])
    sdk.serve([clone, runnodejsscan, runnpm])
