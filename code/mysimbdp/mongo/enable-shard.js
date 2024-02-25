db = db.getSiblingDB("admin");
db.auth("admin", "admin");
sh.enableSharding("airbnb");
sh.shardCollection("airbnb.reviews", { "listing_id": "hashed" });
