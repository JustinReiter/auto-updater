# Auto-Updater

Programmatically updates user projects via Git. Also allows for running a script after `git pull` to restart the project if required. This is intended to be combined with cron to regularly run. **Tested on python 3.10** but should work on other versions.

## Usage

To add a new project to the auto-updater, run the following:
```bash
python main.py -add
```

To view all of the projects currently stored in the config file, run the following:
```bash
python main.py -list
```

To run the auto-updater, run the following:
```bash
python main.py -run
```

### Cron

A sample cronjob to use with this project is to run the updates every 5 min:
```bash
*/5 * * * * cd /home/pi/Desktop/auto-updater/ && python3 main.py -ru
```

## Notes

If a `run-script` is provided, then the auto-updater will run the script after updating the project.
