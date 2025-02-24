#!/usr/bin/env python3
import os
import re
import sys
import semver
import subprocess


def git(*args):
    return subprocess.check_output(["git"] + list(args))


def tag_repo(tag):
    url = 'https://github.com/' + os.environ["GITHUB_REPOSITORY"]

    # Transforms the repository URL to the SSH URL
    # Example input: https://gitlab-ci-token:xxxxxxxxxxxxxxxxxxxx@gitlab.com/threedotslabs/ci-examples.git
    # Example output: git@gitlab.com:threedotslabs/ci-examples.git
    push_url = re.sub(r'.+@([^/]+)/', r'git@\1:', url)

    git("remote", "set-url", "--push", "origin", push_url)
    git("tag", tag)
    git("push", "origin", tag)


def bump(latest):
	ver = semver.VersionInfo.parse(latest)
	major = int(os.environ["major"])
	minor = int(os.environ["minor"])
	
	if (ver.major != major):
		return semver.bump_major(latest)
	elif (ver.minor != minor):
		return semver.bump_minor(latest)
	else:
		return semver.bump_patch(latest)


def main():
    try:
        latest = git("describe", "--tags").decode().strip()
    except subprocess.CalledProcessError:
        # No tags in the repository
        version = "0.0.1"
    else:
        # Skip already tagged commits
        if '-' not in latest:
            print(latest)
            return 0

        version = bump(latest)

    tag_repo(version)
    print(version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
