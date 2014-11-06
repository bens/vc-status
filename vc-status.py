#!/usr/bin/python

from __future__ import print_function
from stgit.commands import common
import stgit
import hglib

def show_queued(applied, unapplied):
    string = ''
    if len(applied) > 1 and len(unapplied) > 0:
        string += "[%d|%s|%d]" % (len(applied)-1, applied[-1], len(unapplied))
    elif len(applied) == 1 and len(unapplied) > 0:
        string += "[%s|%d]" % (applied[-1], len(unapplied))
    elif len(applied) >= 1 and len(unapplied) == 0:
        string += "[%d|%s]" % (len(applied)-1, applied[-1])
    elif len(applied) == 0 and len(unapplied) > 0:
        string += "[|%d]" % (len(unapplied))
    return string

def check_hg():
    repo = hglib.open()
    def query(cmd):
        return [x for x in repo.rawcommand([cmd]).split('\n') if x != '']
    summary   = repo.summary()
    branch    = summary['branch']
    changed   = "" if summary['commit'] else "+"
    applied   = query('qapplied')
    unapplied = query('qunapplied')

    print("(%s%s%s)" % ( branch
                       , show_queued(applied, unapplied)
                       , changed
                       ), end='')

def check_git():
    directory = common.DirectoryHasRepositoryLib()
    try:
        directory.git_dir
        directory.setup()
        repo      = directory.repository
        branch    = repo.current_branch_name
        tree      = repo.get_tree(repo.head_ref)
        w_changed = "" if repo.default_iw.worktree_clean() else "+"
        i_changed = "" if repo.default_index.is_clean(tree) else "!"

        try:
            stack     = repo.current_stack
            applied   = stack.patchorder.applied
            unapplied = stack.patchorder.unapplied
        except stgit.lib.stack.StackException:
            # stg not initialised
            applied   = []
            unapplied = []

        print("(%s%s%s%s)" % ( branch
                             , show_queued(applied, unapplied)
                             , i_changed
                             , w_changed
                             ), end='')
    except common.DirectoryException:
        # not a git repository
        pass

try:
    check_hg()
except:
    check_git()
