
# This will be ignored
You can have more content in here if it helps you. The script will only take what it's looking for.

## Header levels don't matter
Well, to you they probably do. But as long as they are named appropriately, the headers that the script cares about can be at any level.

### Title
Weak Kerberos Authentication

## CVSS
The script ignores this even if it finds it, and submits an "empty" hard-coded CVSS vector for you to edit in SysReptor. Could change in the future if there's enough interest.

### Summary

Kerberoasting is an attack that exploits weak Kerberos authentication.

Note that the script will **respect** your `formatting`, so you should still find these line breaks, bolds, backticks, etc. on SysReptor. It will only trim empty lines at the start and end of each section.

1. This numbered list
2. should be there too,
3. but always check the outcome in SysReptor.

```
It should even support code blocks!
```

The only thing we don't support (for now? Probably for a long while to be honest...) is images. It just gets too complicated. So you'll have to add those in SysReptor.

This applies to every section that takes text, so this one (`summary`), `title`, `impact` and `recommendation`. Ah and `description` too.

### Impact
Much severe. Very impact. Wow!

### This will also be ignored
And the order of the sections also doesn't matter.

### Recommendation
I think you get the picture by now. Onto the special sections...

### References
- This section must be in list format. Everything not in a list item will be ignored.
- http://youcanwritewhateveryouwantthough.com
- I don't think SysReptor cares.

## Affected components
* This section also must be in list format. Note that asterisk lists are also supported.
* If you're a heretic you can also mix dashes and asterisks, the script won't care.
* By the way, the script turns spaces between words in titles into underscores. That's how this ends up in `affected_components`.

# Description
Oh cool! I just realised that you can write the "Finding Evidence" here, and it will go into the "Details" section in SysReptor.

Since we do _our **very** best_ to keep your formatting, it should still be found there.

```
Even code blocks, where you did all that cool hacker stuff!
```

# Miscellaneous
This section totally matters. No just kidding it's also ignored.
