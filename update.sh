#!/bin/bash
cd source/_posts && node ./updateFileTime.nodejs && cd .. && cd .. && git add --all && git commit -m "更新" && git push