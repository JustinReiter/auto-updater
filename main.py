import subprocess
import json
from os.path import exists
import argparse
from datetime import datetime

def log_message(message: str):
    time_str = "[" + datetime.now().isoformat() + "] Auto-Updater: "
    print(time_str + message)
    with open("./logs/{}.txt".format(datetime.now().isoformat()[:10]), 'a') as log_writer:
        log_writer.write(time_str + message + "\n")


def run_auto_updater():
    """
    Runs the auto-updater on all projects
    """

    if not exists('config.json'):
        new_conf = open('config.json', 'x')
        json.dump([], new_conf, indent=4)
        new_conf.close()

    config_file = open('config.json')
    programs = json.load(config_file)

    for program in programs:
        git_output = subprocess.run([
                'git', 'pull', '-C', program['abs_path']
            ], capture_output=True, encoding='utf-8'
        )

        if 'Already up to date.' not in git_output.stdout:
            log_message('Found & applies changes for {}'.format(program['name']))
            if 'run_script' in program:
                rs_output = subprocess.run([program['run_script']], capture_output=True, encoding='utf-8')
                if rs_output.returncode == 0:
                    log_message('Successfully restarted {}'.format(program['name']))
                else:
                    log_message('Failed to restart {}: {}'.format(program['name'], rs_output.stdout))


def run_list_config():
    """
    Lists all projects stored in the auto-updater
    """

    if not exists('config.json'):
        new_conf = open('config.json', 'x')
        json.dump([], new_conf, indent=4)
        new_conf.close()
    
    config_file = open('config.json', 'r')
    programs = json.load(config_file)
    print("Programs:")
    for prg in programs:
        if 'run_script' in prg:
            print("\t{}\n\t\tProj root: {}\n\t\tProj run script: {}".format(prg['name'], prg['abs_path'], prg['run_script']))
        else:
            print("\t{}\n\t\tProj root: {}".format(prg['name'], prg['abs_path']))
    
    if len(programs) == 0:
        print("\t*No projects in the config*")


def run_config_updater():
    """
    Runs the config updater to add a new project to the auto-updater
    """
    
    if not exists('config.json'):
        new_conf = open('config.json', 'x')
        json.dump([], new_conf, indent=4)
        new_conf.close()
    
    config_file = open('config.json', 'r+')
    programs = json.load(config_file)
    new_prog = {}

    new_prog['name'] = input('1) What is the name of the project?\n')
    new_prog['abs_path'] = input('2) What is the absolute path to the project root?\n')
    run_script = input('3) What is the absolute path to the run script to restart the project? (leave blank if no script needed)\n')
    if run_script:
        new_prog['run_script'] = run_script
    
    programs.append(new_prog)
    config_file.seek(0)
    json.dump(programs, config_file, indent=4)
    config_file.close()
    print("\nAdded the following program:\n{}".format(new_prog))


parser = argparse.ArgumentParser(description='Auto-update projects via git')
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-run', help='update all projects', action='store_true')
group.add_argument('-list', help='show all projects for the auto-updater', action='store_true')
group.add_argument('-add', help='add new project to the auto-updater', action='store_true')


args = parser.parse_args()
if args.run:
    run_auto_updater()
elif args.list:
    run_list_config()
elif args.add:
    run_config_updater()
