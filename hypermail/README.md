## HyperMail
An minimalist expressJS email server that delivers core email functionality to all users registered on AGVN.
Mostly decoupled from the main server, as a separate microservice. Can and should be run on another server and domain.

TODO: split this up as a different repo

![](HyperMail-Logo.png)

## Installing Linux Mail
`sudo apt intall mailutils`

## Sending an email
Lets say we want to send an email to `z5258237@unsw.edu.au`.
We want to identify as our domain, `agvn.info`. Hence:

`echo "<MAIL BODY>" | mail -s "<SUBJECT>" -r "noreply@agvn.info" z5258237@unsw.edu.au`

Now clearly, we don't want to do this every single time, let alone manually. So this directory
contains an email server which `/webserver` connects to, in order to send emails.

## MongoDB
Install [mongodb](https://www.mongodb.com/try/download/community) on your machine.

Ensure mongodb server is running -> run `mongod` in an alternate terminal tab.

To access mongoDB shell, type `mongo` in the command line.
To access a database, e.g. `test`, type `use test`.
To view all collections, type `show collections`. If you want to browse the fields in a certain collection, e.g. 'emails' type `db.emails.find()`.

## Registering Emails on Live Service
Ensure SMTP ports, e.g. 25 are open.


## Extensions
- Test the current function that runs the script.
- Test localhost nodemailer.
