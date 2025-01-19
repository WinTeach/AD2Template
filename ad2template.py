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
import shutil
import sys

from pyad import aduser, adquery
from jinja2 import Environment, FileSystemLoader
from tkinter import messagebox

class ad2template:

    def __init__(self):
        # Set up logging configuration
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(lineno)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.getLogger().setLevel(getattr(logging, 'ERROR'))

        exe_dir = os.path.dirname(os.path.realpath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
        os.chdir(exe_dir)

        # Load configuration settings
        self.config = self.getConfig()
        logging.getLogger().setLevel(getattr(logging, self.config['log_level'].upper()))

        logging.info("Initializing ad2template completed")

    def writeTemplates(self):
        try:
            template_vars = self.getAdAttributes()
        except Exception as e:
            logging.error(e)
            messagebox.showerror("Error", str(e))
            exit(1)

        logging.info("Writing Templates")

        env = Environment(loader=FileSystemLoader(self.config['template_folder'], encoding='windows-1252'))
        templates = env.list_templates('.jinja')

        for template in templates:
            jinja_template = env.get_template(template)
            output_filename = template.replace('.jinja', '')
            output_filename = self.replace_vars_in_path(output_filename, template_vars)
            output_path = os.path.join(self.config['output_folder'], output_filename)

            self.create_directory_if_not_exists(os.path.dirname(output_path))

            rendered = jinja_template.render(template_vars)
            with open(output_path, "w", encoding='windows-1252') as f:
                logging.debug(f"Writing {output_filename}")
                f.write(rendered)

        logging.info("All template files written")

        logging.info("Copying non-template files and Folders")
        for item in os.listdir(self.config['template_folder']):
            source_item = os.path.join(self.config['template_folder'], item)
            destination_item = os.path.join(self.config['output_folder'], item)
            destination_item = self.replace_vars_in_path(destination_item, template_vars)

            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item, ignore=shutil.ignore_patterns('*.jinja'), dirs_exist_ok=True)
            elif not item.endswith('.jinja'):
                shutil.copy2(source_item, destination_item)
        logging.info("All non-template files and folders copied")

    def create_directory_if_not_exists(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def replace_vars_in_path(self, path, template_vars):
        for var, value in template_vars.items():
            path = path.replace(f"#{var}#", str(value))
        return path

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
        #Check if config.ini exists
        if not os.path.exists('config.ini'):
            logging.error("config.ini not found")
            messagebox.showerror("Error", "config.ini not found")
            exit(1)

        config = {}

        config_parser = configparser.ConfigParser(interpolation=None)
        config_parser.optionxform = str
        config_parser.sections()

        # Read configuration file
        config_parser.read('config.ini', encoding='utf-8')
        try:
            config_items = config_parser.items("CONFIG")
        except configparser.NoSectionError:
            logging.error("No CONFIG section found in config.ini")
            messagebox.showerror("Error", "No CONFIG section found in config.ini")
            exit(1)

        for key, val in config_items:
            if val.lower() == 'false':
                config[key] = False
            elif val.lower() == 'true':
                config[key] = True
            elif val != '':
                config[key] = os.path.expandvars(val)

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
            #Remove files and Folders
            shutil.rmtree(config['output_folder'])
            os.makedirs(config['output_folder'])

        return config