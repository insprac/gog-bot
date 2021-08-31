# Guild of Guardians Listing Bot

A simple python script that reguarly checks the Guild of Guardian's marketplace 
for new listings and sends notifications to Discord.

The script will create a local file `.gog_token_ids` to keep track of listings
that have already been sent to Discord.

Be aware that there is very little error handling and logging.

### Setup

A Discord webhook URL is required as an environment variable.

```bash
export GOG_BOT_DISCORD_WEBHOOK="<your webhook URL>"
```

The loop frequency can be updated at the top of the file, the default is 60
seconds.

```python
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
