#!/bin/sh
cd source/_posts/ &&node ./updateFileTime.nodejs && cd .. && cd .. && git add --all && git commit -m "$*" && git push origin hexo
