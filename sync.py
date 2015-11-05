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
  'chjj/marked',
  'Polymer/web-component-tester',
  'mochajs/mocha'
];

def GetExistingSubmodules():
  return [l.split()[1] for l in str(git.submodule()).split('\n')
                          if len(l.split()) > 1]

git.submodule.update('--recursive', '--init')

repos = [dict(name=full_name.split('/')[1],
              full_name=full_name,
              ssh_url='git@github.com:%s.git' % full_name)
            for full_name in REPOS]

repos += json.loads(
    str(curl('https://api.github.com/orgs/PolymerElements/repos?per_page=999')))

existing_submodules = GetExistingSubmodules()
repos_submodules = [repo['name'] for repo in repos]

submodules_to_add = \
    [s for s in repos_submodules if s not in existing_submodules]
submodules_to_remove = \
    [s for s in existing_submodules if s not in repos_submodules]

print "To add: ", submodules_to_add
print "To remove: ", submodules_to_remove

for s in submodules_to_remove:
  print 'Removing ' + s + '...'
  git.submodule.deinit('--force', s)
  git.rm(s)

for repo in repos:
  if repo['name'] not in submodules_to_add:
    continue
  print 'Adding ' + repo['full_name'] + '...'
  print repo['ssh_url']
  print repo['name']

  git.submodule.add('--force', repo['ssh_url'], repo['name'])
  print 'Updating ' + repo['full_name'] + '...'
  git.submodule.update('--recursive', '--init')

existing_submodules = GetExistingSubmodules()
print 'Fetching remotes...'
git.submodule.foreach('git', 'fetch', '--tags')
print 'Updating...'
git.submodule.foreach('git', 'checkout', 'origin/HEAD')
git.submodule.foreach('git', 'submodule', 'update', '--init', '--recursive')
