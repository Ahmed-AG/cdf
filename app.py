#!/usr/bin/env python3
from code.cdf import app


# Read config
CONFIG_FILE = "config.d/config.json"
DEFINITIONS_FILE = "config.d/definitions.json"

app(CONFIG_FILE, DEFINITIONS_FILE)