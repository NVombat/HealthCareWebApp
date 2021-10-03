
const mongoose = require("mongoose");

const registerSchema = new mongoose.Schema({
	name: { type: String, required: true },
	email: { type: String, required: true },
	password : { type: String, required: true },
	confirmpassword : { type: String, required: true},
});

module.exports = Login = mongoose.model("user",registerSchema);