db = db.getSiblingDB('twitter');
db.tweets.find({}).count();

