"""This file contains constants used throughout the tests directory."""

import datetime

# Valid Values
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "TestPassword123!"

# FAKE NEIGHBORHOODS
FAKE_NEIGHBORHOODS = [
    "Albany Park",
    "Andersonville",
    "Avondale",
    "Bridgeport",
    "Bronzeville",
    "Chinatown",
    "Edgewater",
    "Englewood",
    "Garfield Park",
    "Gold Coast",
    "Humboldt Park",
    "Hyde Park",
    "Irving Park",
]

# Constants for opening and closing times in full hours
OPENING_TIMES = [
    datetime.time(hour=7, minute=0),
    datetime.time(hour=8, minute=0),
    datetime.time(hour=9, minute=0),
    datetime.time(hour=10, minute=0),
    datetime.time(hour=11, minute=0)
]

CLOSING_TIMES = [
    datetime.time(hour=16, minute=0),
    datetime.time(hour=17, minute=0),
    datetime.time(hour=18, minute=0),
    datetime.time(hour=19, minute=0),
    datetime.time(hour=20, minute=0)
]
