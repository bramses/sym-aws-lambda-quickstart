import json
import sys

from devtools import debug


def handle(event, context) -> dict:
    """
    Escalates or de-escalates depending on the incoming event type.

    For more details on the event object format, refer to our reporting docs:
    https://docs.symops.com/docs/reporting
    """
    print("Got event:")
    debug(event)
    try:
        # get the username from the event
        username = resolve_user(event)
        # update the user in the database
        message = update_user(username, event)
        # if the event type is escalate
        if get_event_type(event) == "escalate":
            # get the reason from the event
            reason = resolve_reason(event)
            # if the reason is 'Every. Villain. Is. Lemons.'
            if reason == 'Every. Villain. Is. Lemons.':
                print(f"formula granted to {username}")
                # return the formula
                return {"body": {"message": 'The Krabby Patty formula is...'}, "errors": []}
            print('no formula!')
            # return a message that the formula was not granted
            return {"body": {"message": f"no formula for you @ {username}!"}, "errors": []}
        else:
            return {"body": {"message": message}, "errors": []}
    except Exception as e:
        debug(e)
        return {"body": {}, "errors": [str(e)]}


def resolve_reason(event) -> str:
    if not checkKey(event, 'fields'):  # if the event does not have a field
        return False
    if not checkKey(event['fields'], 'reason'):  # if the event does not have a reason
        return None
    return event["fields"]["reason"]  # return the reason


def checkKey(dict, key):
    if key in dict.keys():
        return True
    else:
        return False


def resolve_user(event) -> str:
    """
    Placeholder to take the incoming user from the event and resolve to the right
    user id for the system you're escalating the user in.
    """
    return event["actor"]["username"]


def get_event_type(event):
    return event["event"]["type"]


def update_user(username, event) -> str:
    """
    Placeholder to handle updating the given user based on the event type
    """
    event_type = get_event_type(event)
    if event_type == "escalate":
        message = f"Escalating user: {username}"
    elif event_type == "deescalate":
        message = f"Deescalating user: {username}"
    else:
        raise RuntimeError(f"Unsupported event type: {event_type}")
    return message


def resolve_local_json(arg) -> str:
    """Find the right test json file based on the arg"""
    if arg == "-d":
        file = "deescalate.json"
    elif arg == "-e":
        file = "escalate.json"
    else:
        raise RuntimeError(f"Specify either -e or -d, you supplied: {arg}")
    return f"../test/{file}"


def run_local() -> dict:
    """
    This lets you test your function code locally, with an escalate or
    deescalate payload (in the ../test) directory.

    $ python handler.py [-e | -d]
    """
    arg = None if len(sys.argv) < 2 else sys.argv[1]
    path = resolve_local_json(arg)
    with open(path, "r") as payload:
        event = json.load(payload)
    return handle(event, {})


if __name__ == "__main__":
    result = run_local()
    debug(result)
