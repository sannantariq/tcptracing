#!/usr/bin/env python

import configparser
import os
import pwd

def main():
    default_project_dir = os.path.abspath(os.path.dirname(__file__))
    default_db_name = 'test'
    default_username = pwd.getpwuid(os.getuid()).pw_name
    default_password = ''

    project_dir = input(f"Please enter project directory path (default={default_project_dir}):")
    db_name = input(f"Please enter database username (default={default_db_name}):")
    username = input(f"Please enter database username (default={default_username}):")
    password = input(f"Please enter database password (default:{default_password}):")

    project_dir = default_project_dir if project_dir == '' else project_dir
    db_name = default_db_name if db_name == '' else db_name
    username = default_username if username == '' else username
    password = default_password if password == '' else password

    config = configparser.ConfigParser()
    config['PATH'] = {}
    config['POSTGRES'] = {}

    config['PATH']['BASE_DIR'] = project_dir
    
    config['POSTGRES']['NAME'] = db_name
    config['POSTGRES']['USER'] = username
    config['POSTGRES']['PASSWORD'] = password

    config_file_path = f"{project_dir}/configuration.conf"

    print(f"Writing configuration to {config_file_path}")
    with open(config_file_path, 'w') as f:
        config.write(f)

if __name__ == "__main__":
    main()