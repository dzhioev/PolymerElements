#!/usr/bin/python

import json
from sh import curl, grep, git, cut

REPOS = [
  'Polymer/polymer',
  'webcomponents/webcomponentsjs',
  'Polymer/hydrolysis',
  'PolymerLabs/promise-polyfill',
  'PrismJS/prism',
  'web-animations/web-animations-js',
  'chjj/marked'
];

repos = [dict(name=full_name.split('/')[1],
              full_name=full_name,
              ssh_url='git@github.com:%s.git' % full_name)
            for full_name in REPOS]

repos += json.loads(
    str(curl('https://api.github.com/orgs/PolymerElements/repos?per_page=999')))

existing_submodules = str(cut(git.submodule(), f='3', d=' ')).strip().split()

for repo in repos:
  if repo['name'] in existing_submodules:
    print 'Skipped ' + repo['name']
    continue

  print 'Adding ' + repo['full_name'] + '...'
  git.submodule.add(repo['ssh_url'], repo['name'])
  git.submodule.update('--recursive', '--init')
