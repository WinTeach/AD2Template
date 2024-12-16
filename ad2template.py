# ad2template - A Python script that generates files from Jinja2 templates
# using attributes from Active Directory (AD).
# Copyright (C) 2024 Tobias Wintrich
#
# This file is part of ad2template.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import logging
import configparser
from pyad import aduser, adquery
from jinja2 import Environment, FileSystemLoader

class ad2template:

    def __init__(self):
        logging.info("Initializing ad2template")
        self.script_location = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.script_location)

        # Load configuration settings
        self.config = self.getConfig()

        # Set up logging configuration
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(lineno)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.getLogger().setLevel(getattr(logging, self.config['log_level'].upper()))

    def writeTemplates(self):
        # Get Active Directory attributes to use in templates
        template_vars = self.getAdAttributes()

        logging.info("Writing Templates")

        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(self.config['template_folder']))
        for template in env.list_templates():
            jinja_template = env.get_template(template)
            output_filename = template.replace('.jinja', '')
            rendered = jinja_template.render(template_vars)
            # Write rendered template to output folder
            with open(f"{self.config['output_folder']}/{output_filename}", "w") as f:
                logging.debug(f"Writing {output_filename}")
                f.write(rendered)

        logging.info("All template files written")

    def getAdAttributes(self):
        logging.info("Getting AD Attributes")
        username = os.getlogin()

        logging.debug("Getting distinguishedName for user %s", username)
        ad = adquery.ADQuery()
        ad.execute_query(
            attributes=["distinguishedName"],
            where_clause=f"sAMAccountName = '{username}'"
        )

        try:
            distinguished_name = ad.get_single_result()['distinguishedName']
            user = aduser.ADUser.from_dn(distinguished_name)

            logging.debug("Getting allowed attributes for user %s", username)
            allowed_attributes = user.get_allowed_attributes()
            template_vars = {}
            for attribute in allowed_attributes:
                value = user.get_attribute(attribute, False)
                template_vars[attribute] = value
                logging.debug([attribute, value])
                if self.config['print_ad_attributes']:
                    print([attribute, value])

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

        return template_vars

    def getConfig(self):
        logging.info("Reading config.ini")
        config = {}

        configParser = configparser.ConfigParser(interpolation=None)
        configParser.optionxform = str
        configParser.sections()

        # Read configuration file
        configParser.read('config.ini', encoding='utf-8')
        for key, val in configParser["CONFIG"].items():
            if val.lower() == 'false':
                config[key] = False
            elif val.lower() == 'true':
                config[key] = True
            elif val != '':
                config[key] = os.path.expandvars(val)

        logging.debug("Config:\n %s", config)

        # Set default values for missing configuration options
        if 'template_folder' not in config:
            config['template_folder'] = 'templates'

        if 'output_folder' not in config:
            config['output_folder'] = 'output'

        if 'log_level' not in config:
            config['log_level'] = 'ERROR'

        # Ensure template and output folders exist
        if not os.path.exists(config['template_folder']):
            os.makedirs(config['template_folder'])

        if not os.path.exists(config['output_folder']):
            os.makedirs(config['output_folder'])
        elif config['cleanup_output_folder']:
            for file in os.listdir(config['output_folder']):
                os.remove(f"{config['output_folder']}/{file}")

        return config