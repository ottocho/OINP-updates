# onipu

Send email when Ontario Immigrant Nominee Program Updates.

## deploy

Simply deploy on the home directory of your server.

Using [SendGrid](https://sendgrid.com/) to send email.

Only support *Python3*.

``` shell
# python3 pkgs
pip3 install beautifulsoup4 requests html5lib sendgrid

# deploy it in user's base directory
cd ~

# clone repo
git clone https://github.com/ottocho/onipu

#
cd onipu

#
mkdir db private

# put SendGrid key in file
echo 'YOUR_SEND_GRID_KEY' > private/SG_API_KEY

# run
./main.py
```

## on cron

```
24 * * * * cd /home/otto_cho/onipu/ && python3 main.py >>run.log 2>&1
```

## changes

### Dec. 1 2017

first stable version
