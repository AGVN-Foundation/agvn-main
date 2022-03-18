/**
 * Test sending and receiving emails
 */
const email = require('../src/Email.js')

test('Can send an email', () => {
    emailPackage = {
        'from': 'tom@agvn.info', 'to': 'agvn@agvn.info', 'title':
            'Hello', 'body': ''
    }
    return email.send_email()
})

test('Can create an email', () => {
    return email.createEmail()
})
