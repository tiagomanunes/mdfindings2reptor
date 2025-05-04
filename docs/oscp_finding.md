
# Notes
This file represents the expected structure for a finding entry in SysReptor's [OSCP template](https://github.com/Syslifters/sysreptor/blob/main/demo_data/offsec-designs/oscp.toml), as of the time of writing.

It serves as an example usage of the `--custom-fields` flag. Instead of parsing the "native" fields of the tool, you can parse any field marked by a single `*` at the start of the heading. You find the expected titles in each `toml` template file published by SysReptor (look for `[[finding_fields]]`).

So, once you're done writing your findings, you can run something like the following:
```
$ python3 mdfindings2reptor.py /path/to/findings/ --custom-fields --aggregate-only --recurse
```

Every other heading (such as this one) will be ignored. So you can still write any other notes you need in here.

**All** kinds of markdown tags should be supported. Sadly, OSCP seems to be quite screenshot-heavy, and those you'll have to do directly on SysReptor, for reasons that should be obvious.

## Other fields
The "Is Active Directory set?" and "CVSS" fields are not exemplified in the template below. You can try, it probably won't break anything.


# *title
This is the Target Name

# *ip_address
This is, well, the IP address

# *serviceenum
This is the Service Enumeration section.

**Port Scan Results**

| IP Address | Ports Open |
| ------- | ------- |
| TODO   | TODO **TCP:** **UDP:**

TODO
* `nmap -Pn -n 8.8.8.8 | grep open | cut -d/ -f1 | sed 'N;s/\\n/, /g'` for comma separated TCP ports
* `nmap -sU -Pn -n 8.8.8.8 | grep open | cut -d/ -f1 | sed 'N;s/\\n/, /g'` for comma separated UDP ports

**TODO further enumeration results**

# *initialaccess
This is the Initial Access section.

**Vulnerability Explanation:** TODO

**Vulnerability Fix:** TODO

**Steps to reproduce the attack:** TODO

**Proof of Concept Code:** TODO

# *privilegeescalation
This is the Privilege Escalation section.

**Vulnerability Explanation:** TODO

**Vulnerability Fix:** TODO

**Steps to reproduce the attack:** TODO

**Proof of Concept Code:** TODO

# *postexploitation
This is the Post Exploitation section.

**System Proof Screenshot:** TODO
