from twilio.rest import TwilioRestClient
import os, random

def main():
	account = os.environ.get('TWILIO_SID')
	token = os.environ.get('TWILIO_AUTH')
	twilio_num = os.environ.get('TWILIO_NUMBER')
	client = TwilioRestClient(account, token)
	my_phone=[os.environ.get('SAM_NUMBER'),os.environ.get('BILLY_NUMBER'),os.environ.get('JOHN_NUMBER')]

	text_strings = ['Someone rang the doorbell!', 'Someone has rung the doorbell', \
	"Ding Dong! This is the doorbell. There's a person here.", 'Yooooo, come grab the door', \
	'Someone is not at the door. No, wait, sorry, someone is at the door.', \
	'Toughest thing about being a doorbell is no one is ever here to see me.', "Someone's at the door for one of you assholes", \
	"There's either a person or a package at the door for one of you. It would be pretty hard for me to know since I'm a piece of plastic and don't have ears or eyes", \
	'"Beep boop. What is my purpose?"\n"You send doorbell texts"\n"Oh... my god..."\n"Welcome to the club, buddy"', \
	'"One box of CLIF bars coming right up, Mr. Bez--"\n"I mean... ding dong"']

	text_string = random.choice(text_strings)

	for num in my_phone:
		message = client.messages.create(to=num, from_=twilio_num, body=text_string)

if __name__ == '__main__':
  main()
