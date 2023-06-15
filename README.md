<div align="center">
	<img src="https://i.imgur.com/dfGnlNc.png" />
	
</div>

# BRANCH (FAST-API)
<div align="center">
	
![](https://img.shields.io/badge/Repo%20Status-Active-informational?style=flat&logo=GitHub&logoColor=white&color=brightgreen)
![](https://img.shields.io/badge/Python-3.7-informational?style=flat&logo=Python&logoColor=white&color=blue)
![](https://img.shields.io/badge/Build%20Status-Passing-informational?style=flat&logoColor=white&color=success)

</div>	

## Auto Documentation

### Run the server then go to this [`link`](http://127.0.0.1:8000/docs)

# FILE TREE

```
 . <== Root Directory
├──  extractors
│  ├──  dokicloud.py <== The link extractor for the dokicloud provider Example link: https://dokicloud.one/embed-4/8syQ0NzzoziQ?z=
│  ├──  doodstream.py <== The link extractor for the doodstream provider (WARNING: Provider is down a lot) Example link: https://dood.watch/e/6l0auo3uw7yj
│  ├──  mixdrop.py <== The link extractor for the mixdrop provider (WARNING: Provider is down a lot) Example link: https://mixdrop.co/e/0vdnj0mpa88v0q
│  ├──  rabbitstream.py <== The link extractor for the rabbitstream provider Example link: https://rabbitstream.net/embed-4/JMiY67IxPMij?z=
│  ├──  streamlare.py <== The link extractor for the streamlare provider Example link: https://streamlare.com/e/0rZ45Dr7MJWzM81R
│  ├──  servers.py <== Controls the link extractors
│  └──  util
│     ├──  decrypter.py <== Dechipers the encoded url
│     └──  httpclient.py <== Used in the doodstream extractor
├──  pip_api.py <== Main file
├──  pip_api_movies.py <== Used only for film urls
├──  pip_api_shows.py <== Used only for show urls
└──  README.md
```
## Prerequisites
- [`python`](https://www.python.org/) - Used to run the server
- [`pip`](https://www.python.org/) - Needed for dependencies

## Installation

1. Clone or download the repository `git clone https://github.com/Byte-Cats/pip-api.git`
2. Open a terminal and navigate to the directory where the files are located `cd pip-api`
3. Run the following command to start the Flask app `uvicorn pip_api:app --port 5000`

# Usage
## Films
t### /films
### NOTE: ONLY RETURNS FILMS
- **Method:** GET
- **Query Parameter:** q
- **Description:** Returns a list of films based on the search query.
- **Endpoint Example:** [`http://127.0.0.1:8000/films?q=boob`](https://github.com/Byte-Cats/pip-api/blob/main/examples/query/films/films.json)

### /sources

- **Method:** GET
- **Query Parameter:** q
- **Description:** Returns a list of sources for the movie (MOVIES ONLY).
- **Endpoint Example:** [`http://127.0.0.1:8000/films/filmID?q=/movie/watch-space-boobs-in-space-full-56867`](https://github.com/Byte-Cats/pip-api/blob/main/examples/query/films/film-sources.json)

## Shows
### /shows
### NOTE: ONLY RETURNS SHOWS
- **Method:** GET
- **Query Parameter:** q
- **Description:** Returns a list of TV shows based on the search query.
- **Endpoint Example:** [`http://127.0.0.1:8000/shows?q=boob`](https://github.com/Byte-Cats/pip-api/blob/main/examples/query/shows.json)

### /info

- **Method:** GET
- **Query Parameter:** q
- **Description:** Returns information about a TV show. (SHOWS ONLY)
- **Endpoint Example:** [`http://127.0.0.1:8000/shows/showID?q=/tv/watch-booba-full-20324`](https://github.com/Byte-Cats/pip-api/blob/main/examples/query/shows/seasons.json)

### /show

- **Method:** GET
- **Query Parameter:** q
- **Description:** Returns a list of TV shows sources for the episode id (SHOWS ONLY)
- **Endpoint Example:** [`http://127.0.0.1:8000/shows/episodeID?q=1277217`](https://github.com/Byte-Cats/pip-api/blob/main/examples/query/shows/show-sources.json)

## HOW TO STREAM THE LINKS 
## Checkout this [`file`](https://github.com/Byte-Cats/pip-api/blob/main/examples/servers/all-servers.json)

### RABBITSTREAM
```
NOTE: EXAMPLE LINK
mpv "https://b-g-ca-1.feetcdn.com:2223/v3-hls
playback/8cbccbe8f8887b736a596fa0de447cfca7772564fe3a236f3b7a9511ec4f7bfc5404ad2d997c41fa2ac602d74d6b2560c2a8b1534af5ca2f20a57085
241e5733ed703dc660c7dcf60960d3c9c3ab27cdeed9a1ceebf84eec4fa9f629975eded6a0a7e6f1ef658aac2b10892d6b518ec5ad6dbc19c3d5da08ce08feda40d6ab015ffcacae85c82920c299a77c5611491c6b08888d39777777e258907886747b0e/playlist.m3u8"
```
### DOKICLOUD
```
NOTE: EXAMPLE LINK
mpv "https://t-ca-2.24hoursuptodatecdn.net/_v10/8cbccbe8f8887b736a596fa0de447cfca7772564fe3a236f3b7a9511ec4f7bfc5404ad2d997c41fa2ac602d74d6b2560dfb514d628e8dbf28acee1e9e759f05
2f79f34179fbd33f081353a6f7248b876ae35468d20591a310dba24449feb3953709574ddf7110b6f02ec806364f803ab50bc73215f965fc0837d8c461e1b0255/playlist.m3u8"
```
### STREAMLARE
```
NOTE: EXAMPLE LINK
mpv --user-agent="Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0" "https://larecontent.com/video?token=SBFGQV8RCRFbR0dDQAlvHG8cREREHl4CRwYFCgQEHUBAXwNXHV
BcXm8cWXdRY2FAagVKYWkCYX5AcH9QcERSRG8cAgUEBAIBAwoAAG8cBwQdAgsGbxx6BnZrZFhpXllmSn5JaXQeR0l1e11DQ0dsBWNrdF1KfHJlWgBHV1BHUmECB0lSfwFfYAJHSgdYVmxYVmRRVUN7VFILQmdRanx-fXVpcWl9SgpYU
h5DY0JiYwRHa3d-RQd_a3hdQ2lkY1JZVwNsV2QDYUJDCl18BVBkBEkHeEN8fkZ_e2QFRnpnR2tfeWtbf15efwBYbHxVQ2FQbAFhSx5mcARqQFlfUGJxUUF4UGYBZmthUURxZVFZW1wAQQFESlx6VwpmdWB-RV9GfAJ3cAp9RFlVRHdU
VVdgBAJsYVxVXwZaWwNRHnVRUkMLQVp9Hkd7eGd4YV5fQB4GalZcXnhXZQVjRkZ8WkMARWlrX3B9fWwKQV1mC2lrZwQGQXsCaUR9cgZabGJ1a34HA28cCwQEBQoCAB1eQwcMQEdBVlJeDgIRHxFaQxEJEQcEHQILBhFO"
```

### Contributors

- [carrotshniper21](https://github.com/carrotshniper21)
- [4cecoder](https://github.com/4cecoder)

# License


