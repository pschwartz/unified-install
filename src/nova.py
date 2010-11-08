'''
Created on Nov 2, 2010
@author: Philip Marc Schwartz <philip@progmad.com
'''

import os
import urllib2

try:
    import simplejson as json
except ImportError:
    import json

class ManifestImporter:
    def __init__(self, distribution="ubuntu", release="10.04", 
                 host="github.com/piken/unified-install/raw/master/src", ssl=False, 
                 global_manifest="manifest.global"):
        self.distribution = distribution
        self.release = release
        if ssl:
            self.host = "https://"+ host + "/"
        else:
            self.host = "http://"+ host + "/"
        self.__VerifyGlobalManifest(manifest=global_manifest)
        
    def __VerifyGlobalManifest(self, manifest):
        self.global_manifest = json.load(urllib2.urlopen(self.host+manifest))
        if self.distribution in self.global_manifest:
            distro = self.global_manifest[self.distribution]
            if self.release in distro["release"]:
                self.distro_manifest = distro["manifest"]+self.release
                
    def ManifestImport(self):
        if not self.distro_manifest:
            print ManifestImporterError(100)
            exit(100)
        try:
            manifest = urllib2.urlopen(self.host+self.distro_manifest)
            return json.load(manifest)
        except ImportError:
            print ManifestImporterError(200, "%s import attempt failed.", self.distro_manifest)
            exit(200)

class ManifestImporterError(Exception):
    errors = {
              "100":"Distribution manifest not defined.",
              "200":"ManifestError. Manifest does not exist.",
              "300":"VersionError. Release version does not exist.",
        }  
    def __init__(self, status_code, log_message=None, *args):
        self.status_code = status_code
        self.log_message = log_message
        self.args = args
        
    def __str__(self):
        if `self.status_code` in self.errors:
            curr_error = self.errors[`self.status_code`]
        else:
            curr_error = "Unknown Error"
        message = "DistroImporter %d: %s" % (self.status_code,curr_error)
        if self.log_message:
            return message + " ("+ (self.log_message % self.args) +")"
        else:
            return message

def usage():
    print "nova-install [options] [distribution:release]"
    print "Options:"
    print "    --with-mysql                                        - Use MySQL with Nova"
    print "    --mysql-user=[username] - Default: nova             - Set the MySQL Username"
    print "    --mysql-password=[password] - Default: nova         - Set the MySQL Password"
    print "    --network-interface=[interface] - Default: eth0     - Set the Network Interface" 
    print "    --with-ldap                                         - Use LDAP Authentication"
    print "    --branch=[branch]                                   - Set a Launchpad Nova Branch to use" 
    print "    --manifest-host=[host]                              - Set host name to retrieve manifests from"
    print "    --libvirt-type=[type] - Default: qemu               - Set libvirt-type to use"
    print "    --test-install                                      - Run tests after install"

        
def main():
    usage()
    mi = ManifestImporter(ssl=True)
    manifest = mi.ManifestImport()
    for i in manifest["dependencies"]["PckMgr"]:
        print i,manifest["dependencies"]["PckMgr"][i]
        
    
    
if __name__ == '__main__':
    main()