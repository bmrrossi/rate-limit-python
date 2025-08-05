# Rate Limit Implementation

A rate limiter is an important method to building a scalable API. Because it prevents bad users from abusing the API.

A rate limiter keeps a counter on the number of requests received. And reject a request if the threshold exceeds. Requests are rate-limited at the user or IP address level.

## About this project

This project has a single implementation of rate-limit in Python using Flask and Redis.
There is a class called **RateLimit** which manages the requests. A max_limit of requests is set to 10 (just for test)
A counter is implemented using redis and renewed every 60 seconds.

### Main Requirements

 - When the user does the request and the limit is **NOT** exceeded the responde is http status code 202 (Accepted)
 - When the user does the request and the limit is exceeded the response is https status code 429 (Too many requests)

This is the main class with the implementation.

```
class RateLimit:
    def __init__(self, redis_client, max_request=10, window=60):
        self.redis = redis_client
        self.max_request = max_request
        self.window = window

    def allow_request(self, user_id):
        now = time.time()
        key = f"rate_limit:{user_id}"

        pipe = self.redis.pipeline()
        pipe.zadd(key, {now: now})
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zcard(key)
        pipe.expire(key, self.window * 2)

        _, _, request_count, _ = pipe.execute()

        print(request_count)

        return request_count <= self.max_request
```

## Language, tools and libs

I am using these tools and stuff to run this project

 - Python 3.12+ (I believe it would run fine in previous versions (such as 3.11, 3.10, 3.9)
 - Docker 20.10.22 (docker-compose 2.15.1)
 - Flask 3.1.1
 - Redis 7.4.6
 - macOS Sequoia 15.5

## Build and Run

To build and run this project you can type this command:

```
docker-compose up --build -d
```

The application will run on http://localhost:5001 (you can change the port in docker-compose.yml)

To check the logs run this command:

```
docker logs -f rate-limit-web-1
```

## Test

If everyting runs well, you can test it using a http client like Postman and Insomnia (or even your web browser)

Feel free to clone (or fork) this project and play with the parameters.
