// USERS: Verificar índice en email (login o registro)
db.users.find({ email: "test@example.com" }).explain("executionStats")

// USERS: Verificar índice en createdAt
db.users.find().sort({ createdAt: -1 }).limit(1).explain("executionStats")


// RESTAURANTS: Verificar índice multikey en categories
db.restaurants.find({ categories: "Italiana" }).explain("executionStats")

// RESTAURANTS: Verificar índice en createdAt
db.restaurants.find().sort({ createdAt: -1 }).limit(1).explain("executionStats")


// MENU_ITEMS: Verificar índice compuesto en restaurantId + name
db.menu_items.find({ restaurantId: ObjectId("000000000000000000000000") }).sort({ name: 1 }).explain("executionStats")

// MENU_ITEMS: Verificar índice de texto
db.menu_items.find({ $text: { $search: "pizza" } }).explain("executionStats")


// ORDERS: Verificar índice compuesto en userId + createdAt
db.orders.find({
  userId: ObjectId("000000000000000000000000"),
  createdAt: { $gte: ISODate("2024-01-01T00:00:00Z"), $lte: ISODate("2024-12-31T23:59:59Z") }
}).explain("executionStats")

// ORDERS: Verificar índice multikey en items.menuItemId
db.orders.find({ "items.menuItemId": ObjectId("000000000000000000000000") }).explain("executionStats")


// REVIEWS: Verificar índice compuesto en restaurantId, rating, createdAt
db.reviews.find({
  restaurantId: ObjectId("000000000000000000000000")
}).sort({ rating: -1, createdAt: -1 }).explain("executionStats")

// REVIEWS: Verificar índice simple en userId
db.reviews.find({ userId: ObjectId("000000000000000000000000") }).explain("executionStats")
