from LinkedList import DoubleList


# Need to also make sure that the Story Object can be in a LL node
# replace this max_addition stuff with get_best_addition where get_best_addition is a ML module

def get_max_addition(additions):
    max_addition = None
    # might need to change how this loop iterates
    for i in range(0, len(additions)):
        if i == 0:
            max_addition = additions[i]
        if additions[i].votes > max_addition.book_marks:
            max_addition = additions[i]
    return max_addition


def get_active_additions(story):
    # Need some extra validation to ensure this is a story object
    response = DoubleList()
    # the addition array should be a property on the story
    if story.additions is not None:
        for i in story.unique_indicies:
            #Gets each addition at each index reference
            filtered_additions = filter(lambda x: x.index_reference == i, story)
            #take this out of the for loop
            maxAddition = get_max_addition(filtered_additions)
            if maxAddition is not None:
                response.insert(maxAddition, i)
    return response
