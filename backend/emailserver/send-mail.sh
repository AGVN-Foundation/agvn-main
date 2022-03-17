#!/bin/bash
# arg 1 - message body
# arg 2 - message title
# arg 3 - email address receiver
# arg 4 - sender address

echo $1 | mail -s $2 -r $4 $3