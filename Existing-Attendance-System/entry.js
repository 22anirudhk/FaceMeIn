const mongoose = require("./db");

// Define the format for all data entries which will be stored.
const EntrySchema = new mongoose.Schema({
    email: {
        type: String,
        index: true
    },
    checkIn: {
        type: Number,
        index: true
    },
    checkOut: {
        type: Number
    }
});

const Entry = mongoose.model("Entry", EntrySchema);
module.exports = Entry;