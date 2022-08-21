# Auto-Updater

Programmatically updates user projects via Git. Also allows for running a script after `git pull` to restart the project if required. This is intended to be combined with cron to regularly run.

## Usage

To add a new project to the auto-updater, run the following:
```bash
./main.py -add
```

To view all of the projects currently stored in the config file, run the following:
```bash
./main.py -list
```

To run the auto-updater, run the following:
```bash
./main.py -run
```

## Notes

If a `run-script` is provided, then the auto-updater will run the script after updating the project.
