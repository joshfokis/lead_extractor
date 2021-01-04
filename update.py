import json
import os
import requests
import logging

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
            logger.debug(f.readline(0))
            f.seek(0)
            return json.loads(f.read())
    except FileNotFoundError as fnf:
        logger.error(fnf)
        logger.log()
        with open('appinfo','w') as f:
            f.write(json.dumps({'version':0,'latest_commit':'a9f12ee889e4d7417d26e0a0b73ad43e56d6ffc1'}))

def get_commits(url):
    with requests.get(url) as r:
        return r.json()

def compare_version(version, commits, url):
    count = 0
    commits = []
    for commit in commits:
        if version != commit.get('sha'):
            count += 1
            commits.append(commit.get('url'))
        else:
            return count, commits
    return count, commits

def update_files(file):
    excluded = [
        '.gitignore',
    ]
    if file.get('filename') in excluded:
        return
    with requests.get(file.get('raw_url')) as rf:
        with open(file.get('filename'),'w') as of:
            for line in rf:
                of.write(line)
    return
        

def update(updates):
    for url in updates:
        with requests.get(url) as r:
            for file in r.get('files'):
                print(file)
                update_files(file)

def updater():
    url = 'https://api.github.com/repos/joshfokis/lead_extractor/commits'

    files = get_files(__file__)
    info = appinfo()
    commits = get_commits(url)
    behind = compare_version(info.get('version'), commits, url)
    print(files)
    print(info)
    print(commits)
    print(behind)

    if behind[0] > 0:
        try:
            update(behind[1])
            info = appinfo()
            info['latest_commit'] = commits[0].get('sha')
            with open('appinfo') as f:
                f.write(json.dumps(info))

        except Exception as e:
            print(f'Failed to update: {e}')
            
            return e
        

    return True