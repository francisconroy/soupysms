import json
from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession  # import session
from pyairmore.services.device import DeviceService
from pyairmore.services.messaging import MessagingService
from pyairmore.data.messaging import MessageType  # TODO update this in the documentation
from enum import Enum

class Roles(Enum):
    USER=1
    APPROVER=2
    UNREGISTERED=3
    UNDEFINED=4


def get_number_role(num_string, json_data):
    role = Roles.UNDEFINED
    for number in json_data["users"].keys():
        if num_string == number:
            role = Roles.USER

    for number in json_data["approvers"].keys():
        if num_string == number:
            role = Roles.APPROVER

    if role == Roles.UNDEFINED:
        role = Roles.UNREGISTERED

    return role




def run(config_file_path, gw_handset_ip):
    # read in the json file
    config_data = None
    with open(config_file_path, 'r') as config_file:
        config_data = json.load(config_file)

    # Connect to the airmore device
    device_ip = IPv4Address(gw_handset_ip)  # need to put your ip
    session = AirmoreSession(device_ip)  # also you can put your port as int

    # you can check if your airmore server is running
    # you better do it before doing anything on your device
    session.is_server_running  # True

    # and before doing anything, you must request access from your device
    # you better turn on your airmore app on your device and watch it
    session.request_authorization()  # True if accepted, False if denied
    # when you request authorization, airmore app on your device will
    # provide a dialogue to accept the authorization, ensure to accept

    # assuming we have done above
    device = DeviceService(session)
    # all services initializes with a session instance

    details = device.fetch_device_details()
    print(details)

    messasging_service = MessagingService(session)

    # Grab the timestamp of the most recent message to allow for processing of new messages only
    head_message = messasging_service.fetch_message_history()[0]  # most recent message
    current_head_timestamp = head_message.datetime

    print(f"Latest message was at {current_head_timestamp}")

    run = True
    while(run):
        # Keep checking for new SMSes
        all_messages = messasging_service.fetch_message_history()
        # Retrieved X messages
        print(f"Got {len(all_messages)} messages")
        # Find new messages
        new_messages = []
        for msg in all_messages:
            if msg.datetime > current_head_timestamp:
                if msg.type == MessageType.RECEIVED:
                    # It's a new message
                    new_messages.append(msg)

        # update the head timestamp
        if len(new_messages):
            current_head_timestamp = new_messages[0].datetime

        # Process the new_messages
        for msg in new_messages:
            # process the new message by checking if the sender is already in one of the lists
            role = get_number_role(msg.phone, config_data)
            print(f"New message received from {msg.phone}: {msg.content}. User has role {role}")



if __name__ == "__main__":
    # temp hard coded temp file name
    run("testconfig.json", "192.168.1.8")