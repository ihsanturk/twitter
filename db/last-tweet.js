db = db.getSiblingDB('twitter');
db.tweets.find({}).sort({datetime:-1}).limit(1);

