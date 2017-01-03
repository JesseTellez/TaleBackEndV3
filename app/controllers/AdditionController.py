def calculate_index_ref(addition):
    if addition.parent_reference is not None:
        return addition.parent_reference.index_reference + 1
    return 0

def generate_index_reference(parent):
    if parent is not None:
        return 0 if parent.index_reference is None else parent.index_reference + 1
    else:
        return None


def change_active_addition():
    '''Publisher for the change event of an active addition'''
    '''the UI will be the subscriber and update the story real-time'''
    pass