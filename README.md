# Youtube caption extracter and processing the words 

Youtube caption  fetches newly uploaded  captions from your favourite youtube channels and process it to get list of words used in the video and store it in mysql database. Main goal of this project is to improve your english voccabolory. Newly added words are sent to telegram group.

  - Unlimited youtube channels
  - Telegram notification
  - fetches in realtime as soon videos are uploaded 



### Installation



Install the dependencies and devDependencies .

```sh
$ git clone https://github.com/nikkkkhil/youtube_caption.git
$ cd youtube_caption
$ pip install -r requirements.txt 
$ configure telegram api and channel id in code and create mysql databases with Database as database name and dictionary with column words, channel with column url tables.
$ ./ytcaption.py -l youtube_channel_link1 youtube_channel_link2 youtube_channel_link3 .....
```




### Todos

 - Process words more better 
 - Add Night Mode

License
----

MIT


**Free Software, Hell Yeah!**


