import uuid

pending_confirmations = {}


def create_confirmation():

    confirmation_id = str(uuid.uuid4())

    pending_confirmations[confirmation_id] = True

    return confirmation_id


def is_valid_confirmation(confirmation_id: str):

    return pending_confirmations.get(confirmation_id, False)


def remove_confirmation(confirmation_id: str):

    pending_confirmations.pop(confirmation_id, None)