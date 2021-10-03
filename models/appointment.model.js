const mongoose = require("mongoose");

const appointmentlist = new mongoose.Schema({
  doctorname: { type: String, required: true },
  patientname: { type: String, required: true },
  date : { type: String, required: true },
  problem : { type: String, required: true },
});

module.exports = Appointment = mongoose.model("appointment", appointmentlist);