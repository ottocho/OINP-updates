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
mkdir db

# set config for email sending
vim ./config.py

    SG_API_KEY = 'YOUR_SEND_GRID_KEY'

    EMAIL_RECVERS = [
        'RECVER1@z.com',
        'RECVER2@z.com',
    ]
    EMAIL_DEVS = [
        'DEV@z.com',
    ]
    EMAIL_SENDER = 'SENDER@z.com'

# run
./main.py
```

## on cron

```
*/5 *  *   *   *    cd /home/otto_cho/OINP-updates/ && TZ='America/New_York' python3 main.py >>run.log 2>&1
```
