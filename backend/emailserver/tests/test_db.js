// connect to database local
// create schema emails
// create a user, create an email, add to database

var Mongoose = require('mongoose').Mongoose
var mongoose = new Mongoose()

var MockMongoose = require('mock-mongoose').MockMongoose
var mockMongoose = new MockMongoose(mongoose)

var database = require('../src/DB.js')

const db = makeGlobalDatabase()

function cleanUpDatabase(db) {
    db.cleanUp()
}

// NOTE: can change to before and after each test
beforeAll(() => {
    return db.clear().then(() => {
        return db.insert({
            'email_id': 'user', 'emails': [
                { 'from': 'user@agvn.info', 'to': 'agvn@agvn.info', 'title': 'RECOMMEND ACTION', 'body': 'Take action on the current flooding in NSW' },
                { 'from': 'user2@agvn.info', 'to': 'user@agvn.info', 'title': 'Hello', 'body': '' }
            ]
        })
    })
})

afterAll(() => {
    cleanUpDatabase(db)
})

test('Can build email schema', () => {
    // need to do this in a mock database
    return db.buildEmailSchema()
})

test('Can find an email', () => {
    return db.find('thing', {}, results => {
        expect(results.length).toBeGreaterThan(0)
    })
})
