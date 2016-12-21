import redis

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
    '''
    key = 'story:{storyid}:likes'.format(storyid=story_id)
    value = '{userid}'.format(userid=user_id)
    r.sadd(key, value)
    key2 = 'user:{userid}:likes'.format(userid=user_id)
    value2 = '{storyid}'.format(story_id)
    r.sadd(key2, value2, key)
    '''
    while True:
        for item in pubsub.listen():
            print item['data']