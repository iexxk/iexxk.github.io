#!/bin/bash
cd source/_posts/ &&node ./updateFileTime.nodejs && cd .. && cd .. && cd image && ./qshell -mac -m qupload LocalUploadConfig && cd .. && git add --all && git commit -m "更新" && git push origin hexo
