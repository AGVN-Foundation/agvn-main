// import send_email_sh from './Email.js'
const emailhandle = require('./Email.js')
const mongoose = require('mongoose')
const database_name = 'local'
mongoose.connect('mongodb://localhost:27017/' + database_name, { useNewUrlParser: true, useUnifiedTopology: true })

const db = mongoose.connection
db.on('error', console.error.bind(console, 'connection error:'))
db.once('open', function () {
    console.log('Connected to MongoDB:' + database_name)
})

exports.buildEmailSchema = function () {
    var modelNameList = mongoose.prototype.modelNames()
    if (modelNameList.includes('UserEmail')) return
    
    // e.g., NOTE: email_id gets turned to email_id@agvn.info
    /**
     *  { 'UserEmail': [
     *      {'email_id' : 'tom', emails: [
     *          {'from': 'tom@agvn.info', 'to': 'agvn@agvn.info', 'title':  
     *              'Hello', 'body': ''}
     *          ]
     *      },
     *      ]
     *  }
     */
    const emailSchema = new mongoose.Schema({
        email_id: String, emails: [{ from: String, to: String, title: String, body: String }]
    })

    /**
     * Allow user to send an email
     */
    emailSchema.methods.send_email = function (to, title, body) {
        /**
         * Algorithm
         *  check if title is not null -> log error and raise exception (RN: return)
         *  use nodemailer to send the mail
         */
        if (!title) return

        sender = this.email_id
        email = { body: body, title: title, to: to }
        account = { address: sender }
        emailhandle.send_email_sh(account, email)

        // if successfully sent, add that email to user's database
        // when an email is sent to this server, handle saving email logic on receiver side
        email_save = { from: sender, to: to, title: title, body: body }
        sender = this.emails.push(email_save)

        console.log("email sent to:", to, title, body)
    }

    const Email = mongoose.model('UserEmail', emailSchema)
}

exports.createEmail = function (user_from, user_to) {
    // NOTE: for testing only
    // create an email for a user and to another user
}
