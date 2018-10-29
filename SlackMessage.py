from slackclient import SlackClient
import os

def messageToSlack(message, channel):
    with open('token.txt') as fh:
        token=fh.read()
    sc = SlackClient(token)

    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='SlackBot',
                icon_emoji=':robot_face:')


