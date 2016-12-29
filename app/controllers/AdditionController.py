def calculate_index_ref(addition):

    if addition.parent_reference is not None:
        return addition.parent_reference.index_reference + 1
    return 0

def make_addition_active(addition):
    pass


def generate_index_reference(parent):
    if parent is not None:
        return 0 if parent.index_reference is None else parent.index_reference + 1
    else:
        return None