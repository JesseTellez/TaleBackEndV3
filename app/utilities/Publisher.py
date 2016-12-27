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