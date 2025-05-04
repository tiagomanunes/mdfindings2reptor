# mdfindings2reptor
If you're like me and
- you prefer to write your penetration test findings close to where you keep your notes,
- you write your notes in Markdown format, and
- you use [SysReptor](https://docs.sysreptor.com/) to create your reports...

... then this script is for you!

SysReptor's [CLI](https://docs.sysreptor.com/cli/projects-and-templates/finding/) lets you automatically push findings to your project, provided that they are in JSON (or TOML) format.
This script bridges that gap by taking your specially crafted (but not too much) notes and transforming them to the expected JSON format.

## Doesn't this depend on the report template?
Yes! See [compatible report templates](docs/compatibility.md) for a breakdown of the current status. Long story short, it is "natively" compatible with Hack The Box CPTS, CBBH, CAPE and CWEE, but probably handles just about anything by using a special flag.

## Features
- Can be passed a single file, multiple files, or a directory. Searches subdirectories if `--recurse` is used. Only `.md` files are processed.
- Searches for content under specific markdown headers (e.g. `# Impact`). Ignores case and header level. See [docs](docs) for examples.
- Maintains your formatting, line breaks, special characters... probably. Always check the outcome on SysReptor.
- Warns you about unexpected things like duplicated, empty or missing sections. If using `--strict` mode, those warnings will become errors.
- Ignores any other content in your markdown files, so you can still use these files for anything else that supports your findings.
- If your report template is different, you can try using the `--custom-fields` flag to parse headings you've manually marked with a `*`.
- No data loss should be possible: it only reads your markdown files, and SysReptor (seemingly, at the time of writing) creates new findings when pushing (as opposed to overwriting any existing ones). At worst, you'll have a bunch of findings to delete in your SysReptor project. It is recommended to test the push on a separate testing project, and to point `reptor` to your final project when you're happy with the results.

## Instructions

### 1: Get reptor
[Get and install reptor](https://docs.sysreptor.com/cli/getting-started/), SysReptor's CLI automation tool. It does other cool things by the way.

### 2: Get this script
```
$ git clone https://github.com/tiagomanunes/mdfindings2reptor.git
```

### 3: Write your findings
#### "Native" structure
From [SysReptor's documentation](https://docs.sysreptor.com/cli/projects-and-templates/finding/), this is the JSON structure they expect for our findings:
```
{
  "status": "in-progress",
  "data": {
    "cvss": "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:N",
    "title": "Reflected XSS",
    "summary": "We detected a reflected XSS vulnerability.",
    "references": [
      "https://owasp.org/www-community/attacks/xss/"
    ],
    "impact": "The impact was heavy.",
    "description": "This is the finding evidence.",
    "recommendation": "HTML encode user-supplied inputs.",
    "affected_components": [
      "https://example.com/alert(1)",
      "https://example.com/q=alert(1)"
    ]
  }
}
```

The script will always use `"in-progress"` for the `status` and an "empty" `cvss` score of `"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N"` (for now). Aside from those, your markdown findings should include the other fields, as content under their respective headers. See [docs](docs) for more examples, but a bare-bones finding that would result in the JSON above could be:

```
# Title
Reflected XSS

# Summary
We detected a reflected XSS vulnerability.

# Impact
The impact was heavy.

# Recommendation
HTML encode user-supplied inputs.

# References
- https://owasp.org/www-community/attacks/xss/

# Affected components
* https://example.com/alert(1)
* https://example.com/q=alert(1)

# Description
This is the finding evidence.
```

Note that for the `title`, `summary`, `impact`, `recommendation` and `description`, the script will directly use the text. For `references` and `affected_components`, it will attempt to parse list items (supporting both `- ` and `* ` list formats).

When you're done writing your findings, time to convert them to JSON!

#### Custom fields
If your report is special with a completely different finding structure (say, like [CDSA](cdsa_finding.md) or [OSCP](oscp_finding.md)), you can:

1. research the expected finding IDs in SysReptor's template (e.g. [here for CDSA](https://github.com/Syslifters/sysreptor/blob/main/demo_data/htb-designs/cdsa.toml), look for `[[finding_fields]]`);
2. use those IDs as your headings, and prefix them with a `*` (e.g. `# *incident_overview`).

Any fields of type "string" and "markdown" will definitely work. No guarantees made for other types.

Note that _only_ those fields marked with the `*` will now be parsed. The scripts works only in native _or_ custom mode.

### 4: Run the script
Lets see some examples.

If you just want to process a bunch of findings:
```
$ python3 mdfindings2reptor.py /path/*.md
```

If the script needs to check with you before doing something it might regret (like overwriting existing JSON files, or proceeding despite one bad markdown file), it will ask.
The aggregated file containing all the findings (`aggregated_findings.json`) will be created in your current working directory. Individual JSON files, one for each Markdown file, will be created in the same directory where their counterpart was found.

If you have all your findings in a tree structure, want to handle them all, don't care about overwriting any previously generated JSON files, and want the world to stop if any of them are not completely filled-in or fail to be processed for some reason:
```
$ python3 mdfindings2reptor.py /path/to/findings/ --recurse --overwrite --strict
```

If you don't like that this generates a bunch of JSON files (one for each Markdown file in fact), and just want the final aggregate, use `--aggregate-only`. You can always go back and convert hand-picked Markdown files, for example if you have already imported everything to SysReptor but suddenly have a new finding to report.

If your report is special and you've used the appropriate headings, use the `--custom-fields` flag:
```
$ python3 mdfindings2reptor.py /path/to/findings/ --custom-fields --aggregate-only --recurse
```

### 5: Push to SysReptor
The script will actually tell you what to do next.
To push a single file to SysReptor: 
```
$ cat <your_file.json> | reptor finding
```

To push all aggregated findings to SysReptor:
```
$ cat aggregated_findings.json | reptor finding
```


### 6: Check that everything is right in SysReptor
Though of course it is!

## Disclaimer
As mentioned in the Features section, no data loss should ever occur. Still, this script is provided as-is. Use at your own risk, and definitely don't blame SysReptor for any issues.
