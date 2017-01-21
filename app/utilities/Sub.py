import redis

'''This is a Test Subscriber that is going to act as the IOS client'''

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
            print item['data']

