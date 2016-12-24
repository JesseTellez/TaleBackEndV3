import redis
import ast

#Treat this as a fake ios client - this is essentially what the ios client is going to do

config2 = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config2)

if __name__ == '__main__':
    channel = 'LikeChannel'
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    while True:
        for item in pubsub.listen():
            if item['data'] != 1:
                dictionary = ast.literal_eval(str(item['data']))
                story_key = 'story:{storyid}:likes'.format(storyid=dictionary["story_id"])
                story_value = '{userid}'.format(userid=dictionary["user_id"])
                r.sadd(story_key, story_value)
                user_like = 'user:{userid}:likes'.format(userid=dictionary["user_id"])
                user_like_value = '{storyid}'.format(storyid=dictionary["story_id"])
                r.sadd(user_like, user_like_value)
                print "User {userid} has liked story {storyid}".format(userid=dictionary["user_id"], storyid=dictionary["story_id"])
            print item['data']



def LikeListener(item):
    channel = 'LikeChannel'
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    if item != 1:
        dictionary = ast.literal_eval(str(item['data']))
        story_key, story_value = parse_story_like_item(dictionary)
        user_like, user_like_value = parse_user_like_item(dictionary)
    else:
        pass
        #delete


    '''Need to send Keys as an array of dictionaries

    -> I can always send an item like this

    keys_values = [{
        key: 'story:{storyid}:likes',
        value: '{storyid}'
    },
    {
        key: 'user:{userid}:likes',
        value: '{storyid}'
    },
    {
        user: user_id
    }
    ]
    '''

def parse_story_like_item(dictionary):
    story_key = 'story:{storyid}:likes'.format(storyid=dictionary["story_id"])
    story_value = '{userid}'.format(userid=dictionary["user_id"])
    return(story_key, story_value)

def parse_user_like_item(dictionary):
    user_like = 'user:{userid}:likes'.format(userid=dictionary["user_id"])
    user_like_value = '{storyid}'.format(storyid=dictionary["story_id"])
    return (user_like, user_like_value)
