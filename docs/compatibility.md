# Compatible report templates
I wrote this (well, a crude version of this) to prepare for the Hack The Box CPTS exam report, so it is known and ready to work with that (see the last section for a relatively obvious caveat).

The following is a breakdown of compatibility with other report templates, and any known issues or otherwise noteworthy things.

## Hack The Box certification report templates

### Compatible
**CPTS**, **CBBH**, **CAPE** and **CWEE**(1) all share the same finding structure, making the script compatible with all of them.

#### Known issues
(1) The **CWEE** report template uses CVSS version 4.0. The script currently sets a "baseline" CVSS version 3.1 string. Uploading the findings will work, but this issue will be pointed out by SysReptor's validator. I hope to fix this shortly.

#### CWE field
The CWE field is currently not set by the script on any of these templates. This may (or may not) come in the future.

### NOT compatible
To be explicit, the CDSA template has a completely different finding structure, so the script is currently not compatible.

## OffSec certification report templates
The script is not currently compatible with any of the OffSec templates.

**OSCP** compatibility is a Work In Progress.

Other templates may (or may not) follow after that.

## Any other report templates
Probably not compatible, unless they have a similar finding structure to Hack The Box's. Feel free to point me in their direction for a closer look.

## Disclaimer: "compatibility" versus "support"
Words are important, so I was careful not to say "supported".

If you need assistance, please feel free to reach out or create an issue, and I'll do my best to help out.

Please understand that this is not a guarantee, and plan accordingly - certification exams are already stressful, make sure you have a plan B in case this (or any) tool fails at the worst possible time.

Also note that it is in the nature of this tool to be dependent on SysReptor's system, so it will lag behind any updates from their side. If you notice that something broke after an update, please reach out and I'll do my best to fix things in a timely fashion. Again, this is not a guarantee.
