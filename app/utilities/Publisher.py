from .. import r

class Publisher():

    '''I can make publisher for if something succeeded or not'''

    channel = 'DefaultChannel'

    def get_channel(self):
        pass

    def create_and_send_message(self, dictionary):
        if self.channel == 'LikeChannel':
            #return number of likes for a story to IOS client
            story = dictionary["story_id"]
            likes = dictionary["likes"]
            message = 'Story {storyid} now has {num_likes} upvotes'.format(storyid=story, num_likes=likes)
            r.publish(self.channel, message)
            return True
        else:
            return False

    def story_changed_event(self, addition_id, index_reference):
        if self.channel == 'AdditionChangedChannel':
            message = 'Addition {additionid} has become the new active addition at index {indexref}'.format(
                additionid=addition_id,
                indexref=index_reference
            )
            r.publish(self.channel, message)