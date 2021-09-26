import requests, time
from JSONConfig import JSONConfig 
from CloudflareAPIClient import CloudflareAPIClient

# ----- Config -----#
configPath = "config.json"
# ----- Config -----#

"""
    Method to get the id for a specific DNS record
"""
def getIdForDnsRecord(dnsDetail, client):
    records = client.getDNSRecordsFromDNSDetail(account.zoneId, dnsDetail)
    # If no details, try with simplified information
    if (len(records) == 0):
        records = client.getDNSRecordsFromSimplifiedDNSDetail(account.zoneId, dnsDetail)

    # If there are still no dnsRecords, error
    if (len(records) == 0):
        print("There are no records with the type: " + str(dnsDetail.dnsType) + " and name: " + str(dnsDetail.name))
        return None
    
    # If there are multiple records, error
    if (len(records) >= 2):
        print("There are multiple records with the type: " + str(dnsDetail.dnsType) + " and name: " + str(dnsDetail.name) + " - Please run the setup script to continue")
        return None
    
    # Update the dns record if we have 1 record
    dnsDetail.id = records[0].id
    return dnsDetail

# Load the JSON config
config = JSONConfig(configPath)
cloudflareAccounts = config.getCloudflareAccounts()
minutesBetweenChecks = config.getMinutesBetweenChecks()

# If no config details supplied, error and quit
if (len(cloudflareAccounts) == 0):
    print("No valid config file supplied - quitting")
    quit()

# If the minutes between checks has not been included in the config, quit
if (minutesBetweenChecks == None):
    quit()

# Indefinitely check the IP and update the DDNS records if necessary
while (True):
    # Get the current external IP
    currentExternalIp = requests.get("https://api.ipify.org").text

    # For each cloudflare account
    for account in cloudflareAccounts:
        # Setup the cloudflare client
        client = CloudflareAPIClient(apiToken=account.authentication.token, apiKey=account.authentication.key, email=account.authentication.email)
        
        # For each record
        for dnsDetail in account.dnsDetails:
            # If the detail doesn't have an id, try and get one
            if (dnsDetail.id == None):
                detail = getIdForDnsRecord(dnsDetail, client)
                if (detail != None):
                    dnsDetail = detail
                    updatedConfig = config.setIdFromDetails(account.zoneId, dnsDetail)
                    if (updatedConfig):
                        print("ID of record updated successfully")
                    else:
                        print("Config file could not be updated, but id found. Running Cloudflare DDNS update")
                else:
                    continue


            # Get the DNS record from cloudflare
            dnsRecord = client.getDNSRecordById(account.zoneId, dnsDetail.id)

            if (dnsRecord == None):
                print("DNS Record with zoneid: '" + str(account.zoneId) + "' and id: '" + str(dnsDetail.id) + "' could not be found on CLoudflare. Maybe try re-running the setup script")
                continue
            
            # If the IP addresses are not the same, update them
            if (dnsRecord.content != currentExternalIp):
                client.putDNSRecordContents(account.zoneId, dnsDetail.id, currentExternalIp)
                print("DNS record updated with zoneid: '" + str(account.zoneId) + "' and id: '" + str(dnsDetail.id) + "'")

    # Sleep for the specified number of minutes
    time.sleep(minutesBetweenChecks*60)