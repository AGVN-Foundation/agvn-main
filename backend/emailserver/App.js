/**
 * Email application
 * Contains:
 *  - HTTP server for GET and POST (receiving and sending emails)
 *  - FTP server for actually sending the email
 *  - Database of user emails for [user]@agvn.info
 */
const express = require('express')
const DB = require('./src/DB.js')
const mongoose = require('mongoose')
const app = express()
const port = 4690

const SMTPServer = require("smtp-server").SMTPServer
const byteParser = require("mailparser").simpleParser

app.get('/', (req, res) => {
    res.send('Welcome to the A-GVN System\'s Email API')
})

app.get('/build-schema', (req, res) => {
    DB.buildEmailSchema()
})

const Email = mongoose.model('UserEmail')

// Return all emails for user with user email 'req.user'
app.get('/email', (req, res) => {
    // query db for user_email with req.user_email
    const query = mongoose.Model.findOne({ "user_email": req.user_email })
    // If user not found, return 4XX
    if (!query) {
        res.status(404).json({ error: "User not found" })
        return
    }
    // If found, return the entire list of emails as is -> let frontend handle the rest.
    // for all emails in query.emails
    resData = []
    for (x in query.emails) {
        resData.push(x)
    }

    res.status(200).json({ "emails": resData })
})

// Send an email for user 'req.user'
app.post('/send', (req, res) => {
    // query db for user_email with req.from
    const query = mongoose.Model.findOne({ "user_email": req.user_email })
    // If user not found, return 4XX
    if (!query) {
        res.status(404).json({ error: "User not found" })
        return
    }
    // If found, package req.to, req.title, req.body into an object
    resData = { "to": req.to, "from": req.from, "subject": req.title, "text": req.body }
    // Call email.send_email(account, email)
    emails.send_email(resData)

    res.send('Email Sent Successfully!')
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})


// receive smtp requests
// const smtpServer = new SMTPServer({
//     onData(stream, session, callback) {
//         parser(stream, {}, (err, parsed) => {
//             if (err) console.log("Something went wrong ->", err)
//             stream.on("end", callback)
//         })

//     },
//     disabledCommands: ['AUTH']
// })

// smtpServer.listen(25, "127.0.0.1")
