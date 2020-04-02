// Dependencies
// =============================================================
var express = require("express");
var path = require("path");

// Sets up the Express App
// =============================================================
var app = express();
var PORT = 5000;

// Sets up the Express app to handle data parsing
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
// console.log("HEYYY")

// Routes
// =============================================================
// Basic route that sends the user first to the AJAX Page
app.get("/", function(req, res) {
    console.log("HEYYY")
    res.sendFile(path.join(__dirname, "./view/landing.html"));
});

// app.get("/test2", function(req, res) {
//     res.sendFile(path.join(__dirname, "login.html"));
// });

// app.get("/test2", function(req, res) {
//     return res.json(characters);
// });

// app.post("/test2", function(req, res) {
//     var newCharacter = req.body;
//     res.json(newCharacter);
// });

// Starts the server to begin listening
// =============================================================
app.listen(PORT, "127.0.0.1",function() {
    console.log("App listening on PORT " + PORT);
});