#!/usr/bin/env python3
from code.cdf import cdf


# Read config
CONFIG_FILE = "config.d/config.json"
DEFINITIONS_FILE = "config.d/definitions.json"

cdf(CONFIG_FILE, DEFINITIONS_FILE)