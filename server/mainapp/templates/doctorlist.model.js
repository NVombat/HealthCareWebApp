const mongoose = require("mongoose");

const doctorlist = new mongoose.Schema({
  name: { type: String, required: true },
  category: { type: String, required: true },
  specialist : { type: String, required: true },
});

module.exports = Doctor = mongoose.model("doctor", doctorlist);