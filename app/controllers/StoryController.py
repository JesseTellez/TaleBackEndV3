from sets import Set

class Controller:
    stories = []
    def __init__(self, story_array):
        self.stories = story_array

    def get_active_additions(self, story):
        pass

    def get_unique_indicies(self, story):

        """Adjust this """
        if story.additions <= 0:
            return 0
        index_array = []
        for add in story.additions:
            index_array.append(add.index_reference)
        return Set(index_array)

    def addition_added_to_story(self):

        '''publisher of the event of an addition being added to a select story'''
        pass


