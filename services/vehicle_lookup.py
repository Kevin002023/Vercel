import os
import requests
import xml.etree.ElementTree as ET

CARTELL_USERNAME = os.getenv("CARTELL_USERNAME")
CARTELL_PASSWORD = os.getenv("CARTELL_PASSWORD")
CARTELL_SERVICE_NAME = os.getenv("CARTELL_SERVICE_NAME", "XML_Cartell_VRM_Fastnet")

def lookup_vehicle(registration: str) -> dict:
    if not CARTELL_USERNAME or not CARTELL_PASSWORD:
        raise Exception("Cartell credentials not loaded")

    url = "https://api.cartell.ie/secure/xml/findvehicle"
    params = {
        "registration": registration,
        "servicename": CARTELL_SERVICE_NAME,
        "xmltype": "rawxml"
    }

    response = requests.get(
        url,
        params=params,
        auth=(CARTELL_USERNAME, CARTELL_PASSWORD),
        timeout=20
    )
    response.raise_for_status()

    xml_text = response.text

    # For now return raw xml as text so you can inspect it
    return {
        "raw_xml": xml_text
    }
