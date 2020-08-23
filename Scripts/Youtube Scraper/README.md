# YouTube Scraper
Windows based live YouTube comments scraper using Selenium and FireFox. 

Generated output file is a tab-separated file.

Working as of 23/08/2020.


Example code
```Python
from stream_scrape import LiveYouTube

Capture = LiveYouTube('youtube link to a live stream','outputfile.txt')
Capture.r()
```
