from sets import Set

def get_active_additions():
    pass

def get_unique_indicies(story):

    """Adjust this """
    if story.additions <= 0:
        return 0
    index_array = []
    for add in story.additions:
        index_array.append(add.index_reference)
    return Set(index_array)

def addition_added_to_story():

    '''publisher of the event of an addition being added to a select story'''
    pass

def reevaluate_active_additions():
    """Helper to change active additions for a story based on their bookmarks"""
    """Should Cache all the bookmark counts for each addition in a story and only run if a bookmark changes the active addition"""
    pass



