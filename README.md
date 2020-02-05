# Vampire

__Vampire__ is an aggressor script which adds a "Mark Owned" right click option to beacons. This allows you to select either the Computer or User (or Default, which will choose based on your user), along with the domain they belong to. There is an additional optional cna script for marking new credentials as owned. Vampire will communicate with your neo4j REST API on localhost:7474 to mark the node as owned.

<img src="Screen_Shot_2019-04-02_at_3.31.18_PM.png" width="30%" style="float: right"> <img src="Screen_Shot_2019-04-02_at_3.31.54_PM.png" width="30%" style="float: left">
<br style="clear: both">

How to use
---

 0. Put `vampire.cna`, `vampire_creds.cna`, and `owned_utils.py` in the root of your cobaltstrike folder
 1. `chmod u+x owned_utils.py`
 1. Load `vampire.cna` and `vampire_creds.cna` into Cobalt Strike through the Script Manager
 1. Rain shells
 2. Start neo4j and BloodHound as normal
 2. Run BloodHound data collection and import data
 3. Right click your beacon(s) and mark them as owned
 4. Run logonpasswords

Considerations
---

 - neo4j must be running on localhost, on the standard port - 7474
 - Your neo4j database creds should be Kali standard `neo4j:BloodHound` (you can change the base64 in `owned_utils.py` otherwise)
 - `echo -n 'neo4j:yourpassword' | base64` and then replace the auth in owned_utils.py

Benefits
---

 - Never miss an attack path
 - Quickly keep up with other team members' movement

How it works
---

 0. Uses `owned_utils.py` to query the list of domains from neo4j
 1. Obtain user selection
 2. Foreach selected beacon ID:
 3. Append `@` + the specified domain to the user/computer name
 4. For `Default`, it will choose based on whether you're a local admin
 4. Uses `owned_utils.py` to query the neo4j REST API
    - `'START n = node(*) WHERE lower(n.name) = "' + nodelabel.lower() + '" SET n.owned = TRUE'`

---
 
 1. Listens for the `on credentials` callback
 1. Loops through all the credentials, keeping an internal state
 1. Optionally excludes 32 byte passwords (NTLM hashes - see $ignore_hash)
 1. Reconstructs a valid domain for the user
 1. Checks the user exists
 1. Marks new credentials as owned

Author
---

Patrick Hurd
