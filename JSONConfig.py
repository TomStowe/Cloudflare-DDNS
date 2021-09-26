import json, shutil, os
from models.CloudflareDNSAccount import CloudflareDNSAccount
from models.CloudflareAuthenticationDetails import CloudflareAuthenticationDetails
from models.CloudflareDNSDetails import CloudflareDNSDetails

"""
    Class for reading and loading the JSON config
"""
class JSONConfig:
    __configJSON = {}
    __jsonConfigPath = None

    """
        Constructor for the JSON Config
        jsonConfigPath: string - The path for the json config file
    """
    def __init__(self, jsonConfigPath):
        self.__jsonConfigPath = jsonConfigPath
        self.__readConfigFile(jsonConfigPath)

    """
        Gets a list of cloudflare accounts from the config file
        Returns: An array of CloudFlareDNSAccounts if successful, an empty array otherwise
    """
    def getCloudflareAccounts(self):
        cloudflareAccounts = self.__getPropertyFromConfig(self.__configJSON, "cloudflareAccounts")

        if (cloudflareAccounts == None):
            return []
        
        actualAccounts = []

        # Add each account to the list
        for account in cloudflareAccounts:
            auth = self.__getAccountAuth(account)
            dnsDetails = self.__getAccountDNSDetails(account)
            zoneId = self.__getAccountZoneId(account)

            # If any of the fields are None, ignore the account
            if (auth == None or dnsDetails == None or zoneId == None):
                continue

            actualAccounts.append(CloudflareDNSAccount(authentication=auth, zoneId=zoneId, dnsDetails=dnsDetails))

        return actualAccounts

    """
        Set the id of a specific detail and save it to the file
        zoneID: string - The zone id of the dns details to set
        dnsDetail: CloudflareDNSDetail - The dns detail to set the id of
        returns: bool - True if the update was successful, false otherwise
    """
    def setIdFromDetails(self, zoneId, dnsDetail):
        cloudflareAccounts = self.__getPropertyFromConfig(self.__configJSON, "cloudflareAccounts")
        if (cloudflareAccounts == None):
            return False

        # Update the detail
        for account in cloudflareAccounts:
            for detail in self.__getPropertyFromConfig(account, "dnsDetails"):
                if (dnsDetail == detail):
                    detail["id"] = dnsDetail.id
                    
        return self.saveAccounts(cloudflareAccounts)

    """
        Saves the accounts in the config file
        accounts: CloudflareDNSAccounts[] - The list of the accounts to be saved
        Returns: bool - True if successful, false otherwise
    """
    def saveAccounts(self, accounts):
        self.__configJSON["cloudflareAccounts"] = accounts
        try:
            # Save to tmp file
            f = open(self.__jsonConfigPath + "tmp", "w")
            f.write(json.dumps(self.__configJSON, indent=4, sort_keys=True))
            f.close()

            # Overwrite json config
            os.remove(self.__jsonConfigPath)
            shutil.copyfile(self.__jsonConfigPath + "tmp", self.__jsonConfigPath)
            os.remove(self.__jsonConfigPath + "tmp")
            return True
        except:
            print("Could not update config file")
            return False

    """
        Get the number of minutes between checks for the DDNS checker
        Returns: int - The number of minutes that should elapse between a DDNS check
    """
    def getMinutesBetweenChecks(self):
        return self.__getPropertyFromConfig(self.__configJSON, "minutesBetweenChecks")

    """
        Get the authentication for a specific cloudflare account
        account: jsonObject - The account to get the DNS details for
        returns: CloudflareAuthenticationDetails - The authentication details for the cloudflare account
    """
    def __getAccountAuth(self, account):
        authenticationDetails = self.__getPropertyFromConfig(account, "authentication")
        token = self.__getPropertyFromConfig(authenticationDetails, "token", noError=True)
        key = self.__getPropertyFromConfig(authenticationDetails, "key", noError=True)
        email = self.__getPropertyFromConfig(authenticationDetails, "email", noError=True)

        # Check that either the token, or the key and email have been included, otherwise return None
        if (not (token != None or (key != None and email != None))):
            print("Account authentication details invalid, either enter a token or a key and email")
            return None
        
        return CloudflareAuthenticationDetails(token=token, key=key, email=email)

    """
        Get the DNS details for a specific cloudflare account
        account: jsonObject - The account to get the DNS details for
        returns: CloudflareDNSDetails[] - A list of cloudflare dns details
    """
    def __getAccountDNSDetails(self, account):
        dnsDetails = self.__getPropertyFromConfig(account, "dnsDetails")
        if (dnsDetails == None):
            return None

        details = []

        for detail in dnsDetails:
            id = self.__getPropertyFromConfig(detail, "id", noError=True)
            dnsType = self.__getPropertyFromConfig(detail, "type")
            name = self.__getPropertyFromConfig(detail, "name")
            ttl = self.__getPropertyFromConfig(detail, "ttl", noError=True)
            proxied = self.__getPropertyFromConfig(detail, "proxied", noError=True)

            details.append(CloudflareDNSDetails(id=id, dnsType=dnsType, name=name, ttl=ttl, proxied=proxied))

        return details
    
    """
        Get the zoneID for a specific cloudflare account
        account: jsonObject - The account to get the DNS details for
        returns: string - The cloudflare zoneId
    """
    def __getAccountZoneId(self, account):
        return self.__getPropertyFromConfig(account, "zoneId")


    """
        Get a specific property from the config file
        json: jsonObject - The json object to get the value from the key
        key: string - The key of the property to get
        noError: bool (False) - Whether or not to show error messages
        Returns: The value of the key if successful, None otherwise
    """
    def __getPropertyFromConfig(self, json, key, noError=False):
        try:
            val = json[key]
            if (val == ""):
                if (not noError):
                    print("The key '" + str(key) + "' has not been assigned a value")
                val = None
            return val
        except KeyError:
            if (not noError):
                print("The key '" + str(key) + "' could not be found in the config")
            return None

    """
        Read the contents of the config file
        Returns true if the config was successfully read, and false otherwise
    """ 
    def __readConfigFile(self, jsonConfigPath):
        try:
            # Read the file
            f = open(jsonConfigPath)
            self.__configJSON = json.load(f)
            f.close()

        # Handle file not openable error
        except OSError:
            print("The config file could not be opened. Does the file at '" + str(configFilePath) + "' exist?")
            return False
        
        # Handle any other errors
        except:
            print("An unknown error occurred")
            return False

        return True
