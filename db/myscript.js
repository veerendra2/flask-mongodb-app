conn = new Mongo();
db = connect("localhost:27017");
db = db.getSiblingDB('nova')
db.config.createIndex({ "name": 1 }, { unique: true })
// Because we want to store "name" as unique key in DB