# experimental, use if python not working
# NOTE: this script simply appends the fetched data to data/temp.txt 
# arg 1 - url to fetch from
# arg 2 - API key

echo "============ NEW DATA =============\n\n" >> ../data/temp.txt
curl $1 -H "X-Api-Key: $2" >> ../data/temp.txt
