# ==================================================================================
#   File:   nanoblesenseservices.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    Handler for Discovery of all of the Nano BLW Sense Services
#
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import json
import logging

class NanoBLESenseServices():
    
    def __init__(self, logger):
        self.logger = logger
        self.load_file()

    def load_file(self): 
        with open('nanoblesenseservices.json', 'r') as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.info(alerts["Alerts"]["NanoBLESense"]["Loaded"].format(self.data))
            print(alerts["Alerts"]["NanoBLESense"]["Loaded"].format(self.data))

    def load_alerts(self):
        with open('alerts.json', 'r') as alerts_file:
            return json.load(alerts_file)
