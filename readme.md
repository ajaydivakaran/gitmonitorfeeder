#GIT monitor feeder

Python script to read commits from repositories and push the commit meta data to ElasticSearch.

##Steps to run:
Refer: [docker-hub](https://hub.docker.com/r/ajaydivakaran/gitmonitorfeeder/)

##Sample config file:

``` javascript
{
"cachePath": "/tmp/cache",
"batchSize": 10,
"indexName": "repo_commits",
"repos": [
{
"friendlyName": "myRepo",
"repoPath": "/tmp/myrepo",
"branches": ["master"],
"contributors": ["Member1", "Member2", "Member3"]
}
],
"esUrl": "http://elasticsearch:9200"
}
```