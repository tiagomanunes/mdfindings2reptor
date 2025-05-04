
# Notes
This file represents the expected structure for a finding entry in SysReptor's [CDSA template](https://github.com/Syslifters/sysreptor/blob/main/demo_data/htb-designs/cdsa.toml), as of the time of writing.

It serves as an example usage of the `--custom-fields` flag. Instead of parsing the "native" fields of the tool, you can parse any field marked by a single `*` at the start of the heading. You find the expected titles in each `toml` template file published by SysReptor (look for `[[finding_fields]]`).

So, once you're done writing your findings, you can run something like the following:
```
$ python3 mdfindings2reptor.py /path/to/findings/ --custom-fields --aggregate-only --recurse
```

Every other heading (such as this one) will be ignored. So you can still write any other notes you need in here.

**All** kinds of markdown tags should be supported. I'm afraid you'll still need to do screenshots directly on SysReptor, for reasons that should be obvious.

## Other fields
The "Incident Severity" and "Incident Status" fields are combo-boxes, and are not exemplified in the template below. But hey maybe the system will understand it if you pass a string, you can try, it probably won't break anything.


# *title

TODO TO BE FILLED BY THE SECURITY ANALYST

# *incident_id

TODO TO BE FILLED BY THE SECURITY ANALYST

# *incident_overview

TODO TO BE FILLED BY THE SECURITY ANALYST

# *key_findings

TODO TO BE FILLED BY THE SECURITY ANALYST

# *immediate_actions

TODO TO BE FILLED BY THE SECURITY ANALYST

# *stakeholder_impact

TODO TO BE FILLED BY THE SECURITY ANALYST

# *affected_systems

Highlight all systems and data that were either potentially accessed or definitively compromised during the incident. If data was exfiltrated, specify the volume or quantity, if ascertainable.

TODO TO BE FILLED BY THE SECURITY ANALYST

# *evidence_sources

Emphasize the evidence scrutinized, the results, and the analytical methodology employed. Each detection should be elucidated step by step, inclusive of the associated data sources, SIEM queries, and tool commands.

TODO TO BE FILLED BY THE SECURITY ANALYST

# *ioc

IoCs are instrumental for hunting potential compromises across our broader environment or even among partner organizations. These can range from abnormal outbound traffic to unfamiliar processes and scheduled tasks initiated by the attacker.

TODO TO BE FILLED BY THE SECURITY ANALYST

# *root_cause

Within this section, detail the root cause analysis conducted and elaborate on the underlying cause of the security incident (vulnerabilities exploited, failure points, etc.).

TODO TO BE FILLED BY THE SECURITY ANALYST

# *timeline

This is a pivotal component for comprehending the incident's sequence of events. The timeline should include:
* Reconnaissance
* Initial Compromise
* C2 Communications
* Enumeration
* Lateral Movement
* Data Access & Exfiltration
* Malware Deployment or Activity (including Process Injection and Persistence)
* Containment Times (can be excluded)
* Eradication Times (can be excluded)
* Recovery Times (can be excluded)

TODO TO BE FILLED BY THE SECURITY ANALYST

# *nature
type = "markdown"
label = "Nature of the Attack"
origin = "custom"
default = """
Deep-dive into the type of attack, as well as the tactics, techniques, and procedures (TTPs) employed by the attacker. 

TODO TO BE FILLED BY THE SECURITY ANALYST

