Supports Mercurial+MQ and Git+StGit

## Usage

Include a call to the script somewhere in your bash prompt:

```
PS1='\u@\h \w$($HOME/bin/vc-status.py)\$ '
```

### Non version controlled repo
```
user@host ~$ 
```

### Normal repo with no changes in the working tree
Shows the current branch name.
```
user@host ~/vc-status(master)$ 
```

### Normal repo with changes in the working tree
The `+` indicates changes.
```
user@host ~/vc-status(master+)$ 
```

### Normal repo with staged changes
The `!` indicates staging.
```
user@host ~/vc-status(master!)$ 
```

### Repo with a patch stack
Shows the current patch, that there are three other patches pushed below `foo`, and one unpushed patch above `foo`.
```
user@host ~/vc-status(master[3|foo|1])$ 
```
