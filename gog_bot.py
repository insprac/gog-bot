import requests as req
import json
import sys
import time
from string import Template

# Configuration you can update
discord_webhook_url = "<REPLACE WITH YOUR OWN>"
loop_frequency = 60 # in seconds

# Configuration you shouldn't update
gog_base_url = "https://gy2601wgv6.execute-api.us-east-1.amazonaws.com"
gog_api_key = "Np8BV2d5QR9TSFEr9EvF66FWcJf0wIxy2qBpOH6s"
discord_template = Template("$remaining/$total remaining, $eth ETH, $usd USD")

def run():
    token_ids = read_token_ids()
    listings = get_listings()
    ethusd = get_ethusd()

    for listing in listings:
        if listing["token_id"] not in token_ids:
            notify(listing, ethusd)
            token_ids.append(listing["token_id"])

    write_token_ids(token_ids)

def get_listings():
    headers = {"x-api-key": gog_api_key}
    path = "/dev/all-orders?tokenAddress=GuildOfGuardians"
    res = req.get(gog_base_url + path, headers=headers)
    listings = json.loads(res.text)
    formatted_listings = []

    for listing in listings:
        formatted_listings.append(format_listing(listing))

    return formatted_listings

def format_listing(listing):
    metadata = json.loads(listing["metadata"])
    eth = convert_eth_value(listing["takerAssetAmount"])

    return {
        "token_id": listing["token_id"],
        "token_address": listing["token_address"],
        "token_proto": listing["token_proto"],
        "name": metadata["name"],
        "image": metadata["image"],
        "rarity": metadata["rarity"],
        "series": metadata["series"],
        "special_edition": metadata["specialEdition"],
        "amount_remaining": listing["assetAmountRemaining"],
        "amount_total": listing["pCount"],
        "price_eth": eth
    }

def listing_url(listing):
    return "https://tokentrove.com/collection/GuildOfGuardians/" + listing["token_proto"]

def convert_eth_value(value):
    return value / 1000000000000000000

def notify(listing, ethusd):
    print("Notifying:", listing["token_id"])

    description = discord_template.substitute(
        remaining=listing["amount_remaining"],
        total=listing["amount_total"],
        eth=listing["price_eth"],
        usd=listing["price_eth"] * ethusd
    )

    embed_data = {
        "title": listing["name"],
        "url": listing_url(listing),
        "description": description,
        "image": {"url": listing["image"]}
    }

    data = {"embeds": [embed_data]}

    req.post(discord_webhook_url, json=data)

def read_token_ids():
    try:
        with open(".gog_token_ids", "r") as reader:
            return reader.read().split("\n")
    except:
        return []

def write_token_ids(ids):
    with open(".gog_token_ids", "w") as writer:
        writer.write("\n".join(ids))

def get_ethusd():
    res = req.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
    data = json.loads(res.text)
    return data["ethereum"]["usd"]

while True:
    try:
        start = time.time()
        run()
        end = time.time()
    except:
        print("Failed to run")

    print("Looped:", end - start, "seconds")

    time.sleep(loop_frequency)

