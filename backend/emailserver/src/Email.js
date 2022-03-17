/**
 * Module to send emails
 */

const nodemailer = require("nodemailer")

exports.send_email = async function (email) {
    // NOTE: ensure this works

    let transporter = nodemailer.createTransport({
        host: "localhost",
        port: 587,
        secure: false,
    })

    let info = await transporter.sendMail({
        from: email.from, // sender address
        to: "bar@example.com, baz@example.com", // list of receivers
        subject: email.title,
        text: email.body,
        // NOTE: unsure about email.html = null
        html: email.html,
    })

    console.log("Message sent: %s", info.messageId)
    console.log("Preview URL: %s", nodemailer.getTestMessageUrl(info))
}

// For now, use this function that simply wraps around send_main.sh
exports.send_email_sh = async function (email) {
    var exec = require('child_process').exec, child

    child = exec('sendmail.sh ' + email.body + ' ' + email.title + ' ' + email.to + ' ' + email.from,
        function (error, stdout, stderr) {
            console.log('stdout: ' + stdout)
            console.log('stderr: ' + stderr)
            if (error !== null) {
                console.log('exec error: ' + error)
            }
        })
    child()
}
