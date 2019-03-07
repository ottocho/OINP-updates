# OINP-updates

Send an email notification when there were any updates from OINP ([Ontario Immigrant Nominee Program](https://www.ontario.ca/page/2019-ontario-immigrant-nominee-program-updates))

Only support *Python3*.

## deploy

Simply deploy on the home directory of your server and serve by crontab.

Using [SendGrid](https://sendgrid.com/) to send email.

``` shell
# python3 pkgs
pip3 install beautifulsoup4 requests html5lib sendgrid

# deploy it in user's base directory
cd ~

# clone repo
git clone https://github.com/ottocho/OINP-updates

#
cd OINP-updates

#
mkdir db private

# put SendGrid key in file
echo 'YOUR_SEND_GRID_KEY' > private/SG_API_KEY

# put send email address in file
echo 'SEND_EMAIL@z.com' > private/SENDER

# put receiver email address in file
echo 'RECVER_EMAIL@z.com' > private/RECVER

# put debugger(developer) email address in file
echo 'DEBUGGER_EMAIL@z.com' > private/DEBUGGER

# run
./main.py
```

## on cron

```
*/5 *  *   *   *    cd /home/otto_cho/OINP-updates/ && TZ='America/New_York' python3 main.py >>run.log 2>&1
```

## changes

### Dec. 1, 2017

* first stable version

### Dec. 5, 2017

* fix the email config error

### Dec. 25, 2017

* send debug information to debugger email

### Dec. 06, 2018

* fix datetime bug

### Mar. 04, 2019

* Due to the OINP service migration from [ontarioimmigration.ca](http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html) to [onratio.ca](https://www.ontario.ca/page/2019-ontario-immigrant-nominee-program-updates), this service is updated to use new their new data source.
* Refactor the code base

