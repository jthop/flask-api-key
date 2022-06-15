#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
	echo "Welcome back.\n"
else
	# Initial commit: diff against an empty tree object
	against=$(git hash-object -t tree /dev/null)
	echo "Welcome to git stranger.\n"
fi

awk '{n=$NF+1; gsub(/[0-9]+$/,n) } { print> "src/__init__.py";}' src/__init__.py
git add ./src/__init__.py

# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --
