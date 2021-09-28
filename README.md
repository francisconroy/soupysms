# soupysms
A basic community SMS broadcast system based around an Android phone acting as an SMS gateway.

## requirements
An android handset with a SIM card running airmore.
Airmore was chosen as I wanted a solution which had both a server and client available for use immediately
The open source project SMSSync looks like a good alternative, but I've got no intention of writing all the code 
for the client at this stage.

## features (MVP)
- Store all registered recipients in a JSON file
- Have a basic validation method, where X approvals are made via SMS before the SMS is broadcast
- Have the ability to mark certain numbers as authorised approvers in the JSON file

## Future features
- Ability to add new authorised approvers by sending a V-Card to the server handset from an authorised approver's number.
- Ability to request a broadcast via a web portal

## Documentation
### Initial setup
The sample configuration JSON file contains some basic default settings and the required JSON sections.
### Subscribing
Send any message to the server handset number. An acknowledgement will be sent out and the new number added to the JSON list
### Unsubcribing 
SMS "STOP" or any variation of that word (upper/lower) to the SMS server and the entry will be removed from the JSON file
### Sending a broadcast message
Send any message to be broadcast to the server handset number. A message requesting approval for the broadcast will be sent 
to all registered authorised approvers.
X approvals will be required before the broadcast begins.
#### Approving a broadcast message
The authorised approvers will receive an SMS message in the following format:
```text
SMS BROADCAST REQUESTED, return Y/yes to authorise transmission. The message contents follow the colon:
This is a test SMS to be broadcast to everyone
```

### Configuration
Please edit the configuration.json file as needed for your application.
Sample phone numbers are from https://fakenumber.org/australia/mobile

#### Fields
- general - contains general setup information
- users - contains entries for non-approvers, people who will only receive broadcast SMS messages
- approvers - contains entries for approvers, people who can approve broadcasts and will also receive SMS broadcasts
