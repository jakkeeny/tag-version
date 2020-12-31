#! bin/bash

pip install semver
python $GITHUB_ACTION_PATH/src/tag-version.py > version