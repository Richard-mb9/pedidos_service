
db = db.getSiblingDB('orders');
db.createCollection('orders');
db.orders.createIndex({ "id": 1 }, { unique: true });