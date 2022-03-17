/**
 * Taken from mongoose docs
 */
const mongoose = require('mongoose')
mongoose.connect('mongodb://localhost:27017/test', { useNewUrlParser: true, useUnifiedTopology: true })

const db = mongoose.connection
db.on('error', console.error.bind(console, 'connection error:'))
db.once('open', function () {
    // we're connected!
    console.log('Connected to MongoDB')
})

// build schema Kitten {'name': 'str'}
const kittySchema = new mongoose.Schema({
    name: String
})

// NOTE: methods must be added to the schema before compiling it with mongoose.model()
// create speak() method that logs a greeting
kittySchema.methods.speak = function () {
    const greeting = this.name
        ? "Meow name is " + this.name
        : "I don't have a name"
    console.log(greeting)
}

// convert to mongodb model with schema name 'Kitten'
const Kitten = mongoose.model('Kitten', kittySchema)
// create kitten with name 'Silence'
const silence = new Kitten({ name: 'Silence' })
console.log(silence.name)

const fluffy = new Kitten({ name: 'fluffy' })
fluffy.speak()

// save fluffy to mongodb
fluffy.save(function (err, fluffy) {
    if (err) return console.error(err)
    fluffy.speak()
})

// find kittens
Kitten.find(function (err, kittens) {
    if (err) return console.error(err)
    console.log(kittens)
})

// find fluffy using built in regex
Kitten.find({ name: /^fluff/ }, callback = () => { console.log('Found fluffy') })
