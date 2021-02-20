#!/usr/bin/env python

import subprocess
import re


colors = {
    'header': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'gray': '\033[90m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}


def run(command, *args):
    args = [command, *args]
    prc = subprocess.Popen(args, stdout=subprocess.PIPE)
    details = prc.stdout.read()
    details = details.decode("utf-8").strip()
    return details


def main():
    diffs = run('arc', 'list')
    matches = re.findall(r'\* ([\w\s]+?)\s+(D\d+): (.*)', diffs)
    diffs_by_msg = {msg: (diff, status) for status, diff, msg in matches}

    commits = run('git', 'log', f'origin/master..', '--format=%H\t%s')
    commits = commits.split('\n')
    commits = [c.split('\t') for c in commits]
    for sha, message in commits:
        diff, status = diffs_by_msg.get(message, ('', ''))
        if status:
            color = ''
            if 'accepted' in status.lower():
                color = colors["green"]
            if 'needs review' in status.lower():
                color = colors["yellow"]
            if 'needs revision' in status.lower():
                color = colors["red"]
            status = f' {color}[{status}]{colors["end"]} '
        print(f' {colors["blue"]}{sha[:8]}{colors["end"]} {colors["bold"]}{diff}{colors["end"]}{status}{message}')


if __name__ == '__main__':
    main()
