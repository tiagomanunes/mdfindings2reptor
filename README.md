# mdfindings2reptor
If you're like me and
- you prefer to write your penetration test findings close to where you keep your notes,
- you write your notes in Markdown format, and
- you use [SysReptor](https://docs.sysreptor.com/) to create your reports...

... then this script is for you!

SysReptor's [CLI](https://docs.sysreptor.com/cli/projects-and-templates/finding/) lets you automatically push findings to your project, provided that they are in JSON (or TOML) format.
This script bridges that gap by taking your specially crafted (but not too much) notes and transforming fitting them to the expected JSON format.

## Features
- Can be passed a single file, multiple files, or a directory. Searches subdirectories if `--recurse` is used. Only .md files are processed.
- Searches for content under specific markdown headers (i.e. `# Title`). Ignores case and header level. See [docs](docs) for examples.
- Maintains your formatting, line breaks, special characters... probably. Always check the outcome on SysReptor.
- Warns you about unexpected things like duplicated, empty or missing sections. If using `--strict` mode, those warnings will become errors.
- Ignores any other content in your markdown files, so you can still use these files for anything else that supports your findings.
- No data loss should be possible: it only reads your markdown files, and SysReptor (seemingly, at the time of writing) creates new findings when pushing (as opposed to overwriting any existing ones). At worst, you'll have a bunch of findings to delete in your SysReptor project. It is recommended to test the push on a separate testing project, and pointing reptor to your final project when you're happy with the results.

## Instructions

### Get reptor
[Get and install reptor](https://docs.sysreptor.com/cli/getting-started/), SysReptor's CLI automation tool. It does other cool things by the way.

### Get this script
```
$ git clone TBD
```

### Write your findings
From SysReptor's documentation, this is the JSON structure they expect for our findings:
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
    "recommendation": "HTML encode user-supplied inputs.",
    "affected_components": [
      "https://example.com/alert(1)",
      "https://example.com/q=alert(1)"
    ]
  }
}
```

The script will always use `"in-progress"` for the status and an "empty" CVSS score of `"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N"` (for now). Aside from those, your markdown findings should include the other fields, as content under their respective headers. See [docs](docs) for more examples, but a bare-bones finding for the JSON above could be:

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
```

Note that for the title, summary, impact and recommendation we directly use the text, while for references and affected_components we will attempt to parse list items (supporting both `- ` and `* ` formats).

When you're done with your findings, time to convert them to JSON!

### Run the script
Lets see some examples. 

If you just want to process a bunch of findings and get prompted for any issues:
```
$ python3 mdfindings2reptor.py /path/*.md
```

If you have all your findings in a tree structure, want to handle them all, don't care about any previously generated JSON files, and want the world to stop if any of them are not completely filled-in:
```
$ python3 mdfindings2reptor.py /path/to/findings/ --recurse --overwrite --strict
```

If you don't like that this generates a bunch of JSON files (one for every Markdown file in fact), and just want the final aggregate, use `--aggregate-only`. You can always go back and convert hand-picked Markdown files, for example if you have already imported everything to SysReptor but suddenly have a new finding to report.

### Push to SysReptor
The script will actually tell you what to do next.
To push a single file to SysReptor: 
```
$ cat <your_file.json> | reptor finding
```

To push all aggregated findings to SysReptor:
```
cat aggregated_findings.json | reptor finding
```


### Check that everything is right in SysReptor
Though of course it is!

## Disclaimer
As mentioned in the Features section, no data loss should ever occur. Still, this script is provided as-is. Use at your own risk, and definitely don't blame SysReptor for any issues.
