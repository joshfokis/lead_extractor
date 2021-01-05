import json
import os
import requests
import logging
from shutil import copy2


log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger(__name__)

# To override the default severity of logging
logger.setLevel('DEBUG')

# Use FileHandler() to log to a file
file_handler = logging.FileHandler("mylogs.log")
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Don't forget to add the file handler
logger.addHandler(file_handler)

def get_files(current_file):
    logger.info('Getting files')
    for dir_path, directory, files in os.walk(os.getcwd()):
        logger.debug(files)
        return files

def appinfo():
    try:
        with open('appinfo') as f:
            logger.info('Loading appinfo')
            f.seek(0)
            return json.loads(f.read())
    except FileNotFoundError as fnf:
        logger.error(fnf)
        logger.info('Creating appinfo')
        with open('appinfo','w') as f:
            f.write(json.dumps({'version':0,'latest_commit':'a9f12ee889e4d7417d26e0a0b73ad43e56d6ffc1'}))

def get_commits(url):
    logger.info("Getting commits.")
    with requests.get(url) as r:
        logger.debug(f'Returned with {len(r.json())}')
        return r.json()

def compare_version(version, commits):
    count = 0
    latest_commits = []
    logger.info('Compairing commit versions.')
    logger.debug(f'{version=}')
    for commit in commits:
        if version != commit.get('sha'):
            logger.debug(f"{version=} -- commit{commit.get('sha')}")
            count += 1
            latest_commits.append(commit.get('url'))
        else:
            return count, latest_commits
    return count, latest_commits

def update_files(file):
    excluded = [
        '.gitignore',
    ]
    if file.get('filename') in excluded:
        return
    logger.info(f'Updating File {file.get("filename")}')
    with requests.get(file.get('raw_url')) as rf:
        with open(file.get('filename'),'w') as of:
            for line in rf:
                of.write(line)
    return
        

def update(updates):
    logger.info('Updating files')
    for url in updates:
        with requests.get(url) as r:
            for file in r.get('files'):
                backup(file.get('filename'))
                update_files(file)

def restore():
    files = get_files()
    logger.info('Restoring backup files')
    for file in files:
        if file.endswith('.bak'):
            logger.info(f'Restoring {file}')
            copy2(file, file.replace('.bak', ''))
            os.remove(file)

def clean_up():
    logger.info('Cleaning backup files')
    files = get_files()
    for file in files:
        if file.endswith('.bak'):
            logger.info(f'Removing {file}')
            os.remove(file)

def backup(file):
    logger.info
    copy2(file, file+'.bak')

def updater():
    url = 'https://api.github.com/repos/joshfokis/lead_extractor/commits'
    files = get_files(__file__)
    info = appinfo()
    commits = get_commits(url)
    behind = compare_version(info.get('latest_commit'), commits)

    if behind[0] > 0:
        try:
            update(behind[1])
            info = appinfo()
            info['latest_commit'] = commits[0].get('sha')
            with open('appinfo') as f:
                logger.info('updating appinfo')
                f.write(json.dumps(info))
            clean_up()
        except Exception as e:
            print(f'Failed to update: {e}')
            restore()
            logger.exception(e)
            return e
        
    return True
