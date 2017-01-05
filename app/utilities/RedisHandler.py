from app import r


def save_to_redis(key_values):

    redis_key = key_values["key"]
    redis_value = key_values["value"]
    type = key_values["type"]

    if type == "user_like":
        # story_key, user_id - user stored in the stories list
        check = r.sismember(redis_key, redis_value)
        print check
        if check == 0:
            r.sadd(redis_key, redis_value)
            #FIGURE OUT HOW TO RETURN COUNT OR DONT HAVE THIS TAKE AND ARRAY
            count = r.scard(redis_key)
            return True, count
        else:
            r.srem(redis_key, redis_value)
            count = r.scard(redis_key)
            return True, count
    elif type == "story_like":
        # user_key, story_id - story_id stored in user list
        #  This needs to be story!!!
        check = r.sismember(redis_key, redis_value)
        if check == 0:
            r.sadd(redis_key, redis_value)
            count = r.scard(redis_key)
            return True, count
        else:
            r.srem(redis_key, redis_value)
            count = r.scard(redis_key)
            return True, count
    else:
        return False, 0
    return False, 0
