# ==================================================================================
#   File:   config.py
#   Author: Larry W Jordan Jr (larouex@gmail.com)
#   Use:    SaS key class for all operations on connections and generation of
#           keys used to connect via DPS and Azure IoT Central
#   Online:   www.hackinmakin.com
#
#   (c) 2020 Larouex Software Design LLC
#   This code is licensed under MIT license (see LICENSE.txt for details)    
# ==================================================================================
import json
import logging

class Config():

    def __init__(self, logger):
        self.logger = logger
        self.load_file()

    def load_file(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)
            alerts = self.load_alerts()
            self.logger.info(alerts["Alerts"]["Config"]["Updated"].format(self.data))
            print(alerts["Alerts"]["Config"]["Updated"].format(self.data))

    def load_alerts(self):
        with open('alerts.json', 'r') as alerts_file:
            return json.load(alerts_file)