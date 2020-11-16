db = db.getSiblingDB('twitter');
db.tweets.find({}, {"_id": 0, "tweet": 1, "capture_delay_sec": 1}).sort({datetime:-1}).limit(10);

