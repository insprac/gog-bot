# Guild of Guardians Listing Bot

A simple python script that reguarly checks the Guild of Guardian's marketplace 
for new listings and sends notifications to Discord.

The script will create a local file `.gog_token_ids` to keep track of listings
that have already been sent to Discord.

Be aware that there is very little error handling and logging.

### Setup

Update the configuation with your own Discord webhook URL and set the loop
frequency (60 seconds by default).

```python
discord_webhook_url = "<REPLACE WITH YOUR OWN>"
loop_frequency = 60
```

You may need to install the `requests` package

```bash
pip install requests
```

### Run

```bash
python gog_bot.py
```
