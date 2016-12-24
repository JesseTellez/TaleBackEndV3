from .. import r


def save_to_redis(key_values):
    for dict in key_values:
        redis_key = dict["key"]
        redis_value = dict["value"]
        type = dict["type"]

        if type == "user_like":
            # story_key, user_id - user stored in the stories list
            check = r.sismember(redis_key, redis_value)
            print check
            if check == 0:
                r.sadd(redis_key, redis_value)
                #FIGURE OUT HOW TO RETURN COUNT OR DONT HAVE THIS TAKE AND ARRAY
                count = r.scard(redis_key)
                return "Saved to story set", count
            else:
                r.srem(redis_key, redis_value)
                count = r.scard(redis_key)
                return "Removed from story set", count
        elif type == "story_like":
            # user_key, story_id - story_id stored in user list
            # This needs to be story!!!
            check = r.sismember(redis_key, redis_value)
            if check == 0:
                r.sadd(redis_key, redis_value)
                return "Saved to user set"
            else:
                r.srem(redis_key, redis_value)
                return "Removed from user set"
        else:
            return "Must Provide A Type."
    return "Dictionary Empty"
