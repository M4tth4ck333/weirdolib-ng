# weirdolib-ng

## Description
(based on the work of derv merkler)
An overworked series of Python 3.x scripts for generating, merging, and sorting and counting wordlist files and db's.
based on bluez scapy networkx and many more 
## Overview

This repository contains a modular network engine designed for advanced penetration testing, network reconnaissance, and automated security assessments. 
Inspired by leading open-source tools and frameworks, the engine integrates classic and modern techniques for network discovery, scanning, exploitation, and reporting.

---

## Features

- **Network Scanning & Enumeration**
  - Automated detection of network interfaces (including monitor mode support)
  - Scanning for wireless networks using system tools (e.g., `iw`)
  - Parsing and structuring scan results into Python objects for further analysis

- **Wireless Network Analysis**
  - Extraction of detailed access point and client information (SSID, BSSID, channel, signal, security, etc.)
  - Support for channel and frequency mapping
  - Management of network and client objects with serialization (JSON import/export)

- **Modular Architecture**
  - Core classes for `WirelessNetwork` and `WirelessClient`
  - Helper functions for MAC address retrieval, signal quality calculation, and interface management
  - Easily extensible for integration with other tools and frameworks

- **Automation & Scripting**
  - Define scan jobs and workflows using tables (lists of dicts) or enums for flexible automation
  - Batch processing and workflow orchestration for repeatable assessments

- **Error Handling & Reporting**
  - Robust error codes and messages for device status, permissions, and scan results
  - JSON-based reporting for integration with other tools or dashboards

---

## Example Workflow

1. **Interface Detection**
   - Automatically list all wireless interfaces and identify those in monitor mode

2. **Network Scanning**
   - Launch scans on selected interfaces and (optionally) specific frequencies
   - Parse scan output and extract structured information on all detected networks

3. **Data Management**
   - Store and manage network and client objects
   - Serialize/deserialize results for later use or reporting

4. **Automation**
   - Use tables or enums to define and execute multiple scan jobs in sequence

---

## Technologies Used

- **Python 3.x**
- **System tools:** `iw`, `iwconfig`
- **Standard libraries:** `subprocess`, `re`, `json`, `datetime`, etc.

---

## Getting Started

1. Clone this repository.
2. Ensure Python 3.x and required system tools (`iw`, `iwconfig`) are installed.
3. Run the main script as root (required for wireless scanning and interface management).
4. Customize scan jobs or extend the engine with your own modules.

---
