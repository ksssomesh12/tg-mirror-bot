#!/bin/bash

cat >~/project/Dockerfile <<EOF
FROM $CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME:$CIRCLE_BRANCH-latest
WORKDIR /usr/src/app
COPY . .
EOF

echo "Dockerfile created for '$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME:$CIRCLE_BRANCH-latest' tag"