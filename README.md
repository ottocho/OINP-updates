# OINP-updates

To send email for updates from [Ontario Immigrant Nominee Program](http://www.ontarioimmigration.ca/en/pnp/OI_PNPNEW.html).

## deploy

Simply deploy on the home directory of your server and serve by crontab.

Using [SendGrid](https://sendgrid.com/) to send email.

Only support *Python3*.

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
24 * * * * cd /home/otto_cho/OINP-updates/ && python3 main.py >>run.log 2>&1
```

## changes

### Dec. 1 2017

first stable version

### Dec. 5 2017

fix the email config error

### Dec. 25 2017

send debug information to debugger email
