import discord
import xml.etree.ElementTree as ET
import requests
import re
from datetime import datetime

# Replace with your bot token
TOKEN = 'MTEzOTA3NjczNTE4MzM3MjQwOA.G5bHSo.0klqcegMmrVZuo5KutDUMeoOVSWwA05rAD2C9c'
GUILD_ID = 1136029996587163808
CHANNEL_ID = 1139269036459425873

# Store the timestamp of the last update
last_update_timestamp = 0

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def fetch_rss_feed():
    # Replace with the URL of the RSS feed
    rss_url = 'https://ctftime.org/event/list/upcoming/rss/'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(rss_url,headers=headers)
    return response

def parse_rss_feed(response):
    root = ET.fromstring(response.content)
    items = []
    for item in root.findall('./channel/item'):
        title = item.find('title').text
        link = item.find('link').text
        description = item.find('description').text
        start_date = item.find('start_date').text  # Extract start_date content
        items.append({'title': title, 'link': link, 'description': description, 'start_date': start_date})
    return items

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    response = fetch_rss_feed()
    parsed_items = parse_rss_feed(response)
    
    current_date = datetime.now()
    
    for item in parsed_items:
        start_time_obj = datetime.strptime(item['start_date'], '%Y%m%dT%H%M%S')
        if start_time_obj > current_date:
            info_list = item['description'].replace('\n', '').split('<br/>')
        
            pattern1 = r'Date: (.+?) &mdash; (.+?) &nbsp;'
            start_time = re.search(pattern1, info_list[1]).group(1)
            end_time = re.search(pattern1, info_list[1]).group(2)
            
            pattern2 = r':\s*(.*)'
            pattern3 = r'<a.*?>(.*?)</a>'
            format = re.search(pattern2, info_list[2]).group(1) + ' | ' + info_list[3].replace('<b>', '').replace('</b>', '')
            try:
                official_url = re.search(pattern2, info_list[4]).group(1)
                event_organizers = re.search(pattern2, info_list[6]).group(1)
                
                embed = discord.Embed(title=item['title'], url=re.search(pattern3, official_url).group(1))
                embed.add_field(name='Start Date', value=start_time, inline=False)
                embed.add_field(name='End Date', value=end_time, inline=False)
                embed.add_field(name='Format', value=format, inline=False)
                embed.add_field(name='CTFtime URL', value=item['link'], inline=False)
                embed.add_field(name='Event Organizer', value=re.findall(pattern3, event_organizers)[0], inline=False)
                embed.set_thumbnail(url=re.search(pattern3, official_url).group(1))
            except:
                official_url = re.search(pattern2, info_list[5]).group(1)
                event_organizers = re.search(pattern2, info_list[7]).group(1)
                
                embed = discord.Embed(title=item['title'], url=re.search(pattern3, official_url).group(1))
                embed.add_field(name='Start Date', value=start_time, inline=False)
                embed.add_field(name='End Date', value=end_time, inline=False)
                embed.add_field(name='Format', value=format, inline=False)
                embed.add_field(name='CTFtime URL', value=item['link'], inline=False)
                embed.add_field(name='Event Organizer', value=re.findall(pattern3, event_organizers)[0], inline=False)
                embed.set_thumbnail(url=re.search(pattern3, official_url).group(1))
            
            guild = client.get_guild(GUILD_ID)
            channel = guild.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)

# Run the bot
client.run(TOKEN)
