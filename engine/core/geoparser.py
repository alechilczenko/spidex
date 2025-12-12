from datetime import datetime
from config import Config

import geoip2.errors
import geoip2.database
from colorama import Fore


'''
Receives an ip address validated by the portscan object and returns a JSON with the geolocation.
'''

def search_geolocation(ip):
    try:
        with geoip2.database.Reader(Config.CITY_DB) as geo_reader:
            response = geo_reader.city(ip)
        with geoip2.database.Reader(Config.ASN_DB) as asn_reader:
            resp = asn_reader.asn(ip)
            return resp.autonomous_system_organization, resp.autonomous_system_number, response.country.name, response.city.name, response.country.iso_code, response.location.latitude, response.location.longitude

    except geoip2.errors.AddressNotFoundError:
        return None

def create_json(ip,banners,hostname,ports,tags):

    org,asn,country,city,iso_code,lat,long = search_geolocation(ip)
    col = {
            "ip": ip,
            "org": org,
            "asn": asn,
            "banners": banners,
            "ports": ports,
            "hostname": hostname,
            "country": country,
            "city": city,
            "country_code": iso_code,
            "latitude": lat,
            "longitude": long,
            "tags": tags,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
    doc = {k:v for k,v in col.items() if v is not None}
    #Formatting output, removig None values
    if tags != None:
        output = F"{Fore.WHITE}{ip} {ports} {tags}"
    else:
        output = F"{Fore.WHITE}{ip} {ports}"

    return doc, output
 