// @author Finn Frankis


const mongoose = require('mongoose');
mongoose.Promise = global.Promise;

mongoose.connect(`mongodb://localhost:27017/robotics-website`, {
  poolSize: 10, bufferMaxEntries: 0, useNewUrlParser: true,useUnifiedTopology: true,
 config: {
   autoIndex: false
 }
});

const db = mongoose.connection;
db.on('error', () => {
 console.error('MongoDB connection error');
 process.exit(1);
});
db.once('open', () => {
 console.log('Successfully connected to MongoDB');
});

module.exports = mongoose;

