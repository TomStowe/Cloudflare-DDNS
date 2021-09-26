# ☁️ Cloudflare DDNS
A simple dynamic domain name server solution for cloudflare.

## ✅ Features
* IPv4 and IPv6 compatible
* Supports multiple DNS records with the same `type` and `name` details
* Secure connection to Cloudflare API using HTTPS
* Open source

## 🔧 Setup
* Download the git repo using `git clone ...`
* Update `config.json` with the following values for each cloudflare domain:
  * Add your authentication details (either your email address and key or your token which is capable of **edit DNS** functionality). Find out more [here](https://developers.cloudflare.com/api/tokens/create)
  * Add the `zoneId`, found [in the overview tab of the cloudflare dashboard](https://community.cloudflare.com/t/where-to-find-zone-id/132913)
  * Add the relevant DNS details (`name` and `type` fields are required) for each DNS record you want to update
* Run `python3 setup.py` to setup the config (this will need to be re-run if you update the DNS records on cloudflare that are stored in the config at any point)
* Schedule the DDNS script to run on startup of the machine. For example using a cron job: run `crontab -e` and add `@reboot /usr/bin/python3 CURRENT_DIRECTORY/main.py`

## 🎓 Licence
This software is released under the [GNU AGPLv3](LICENSE) licence

## 👨 The Author
[Please click here to see more of my work!](https://tomstowe.co.uk)
