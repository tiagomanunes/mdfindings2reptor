# Compatible report templates
I wrote this (well, a crude version of this) to prepare for the Hack The Box CPTS exam report, so it is known and ready to work with that (see the last section for a relatively obvious caveat).

The following is a breakdown of compatibility with other report templates, and any known issues or otherwise noteworthy things.

## Hack The Box certification report templates

### "Natively" Compatible
**CPTS**, **CBBH** and **CAPE** all share the same finding structure, making the script compatible with all of them.

(Note that CWEE also uses the same structure, but the exam requires the report to be in Markdown format, so you may not want to use SysReptor for it. If you somehow still do, note that the CWEE report template uses CVSS version 4.0. The script currently sets a "baseline" CVSS version 3.1 string. Uploading the findings will work, but this issue will be pointed out by SysReptor's validator.)

#### CWE field
The CWE field is currently not set by the script on any of these templates. This may (or may not) come in the future.

### Compatible via `--custom-fields`
The **CDSA** template has a completely different finding structure. You can still use this tool by using specific headings and using the `--custom-fields` flag. [See the docs for a template you can use](cdsa_finding.md).

## OffSec certification report templates

The **OSCP** template has a different finding structure. You can still use this tool by using specific headings and using the `--custom-fields` flag. [See the docs for a template you can use](cdsa_finding.md).

I've personally tested this with my own report, which I cannot say for any other of the OffSec templates. But the custom field approach probably works for those too. Finding the right headings in [SysReptor's templates](https://github.com/Syslifters/sysreptor/blob/main/demo_data/offsec-designs/) will be up to you (look for `[[finding_fields]]`).

## Any other report templates
Probably not "natively" compatible, unless they have a similar finding structure to Hack The Box's offensive certs, but probably compatible using the `--custom-fields` flag. Check out the [CDSA](cdsa_finding.md) and [OSCP](oscp_finding.md) examples of what that would look like.

## Disclaimer: "compatibility" versus "support"
Words are important, so I was careful not to say "supported".

If you need assistance, please feel free to reach out or create an issue, and I'll do my best to help out.

Please understand that this is not a guarantee, and plan accordingly - certification exams are already stressful, make sure you have a plan B in case this (or any) tool fails at the worst possible time.

Also note that it is in the nature of this tool to be dependent on SysReptor's system, so it will lag behind any updates from their side. If you notice that something broke after an update, please reach out and I'll do my best to fix things in a timely fashion. Again, this is not a guarantee.
