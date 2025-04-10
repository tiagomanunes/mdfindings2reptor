
Stuff that's not under a header will also be ignored, unless it's at the end of the file... see the end of the file.

# Title
Directory listing enabled

# Summary
This is a summary.

# IMPACT
You better not have sensitive data in those directories!

Speaking of sensitivity, note that the script will not be sensitive to case in the headers, so write them as you like them. 

It does expect a perfect match, however, so "Impact:" wouldn't be found due to that trailing colon.

## SuMmArY
Uh-oh! This is also a summary! Remember, header levels and case don't matter. One of two things will happen now:

- in normal mode, the script will print a warning and proceed to merge the content of the two "Summary" sections. Up to you to fix it either here or in SysReptor.
- in `--strict` mode, the script will print an error and abort the processing of this file.

# recommendations
Will this section be picked up? Trick question. It will not. Again, the script expects a perfect match, albeit case-insensitive, and looks for "recommendation", not "recommendationS".

# References

## Affected components
* You may have noticed that there was no list of references, just above.
- In normal mode, that's totally fine. In `--strict` mode, the script will print an error and abort the processing of this file.
* This is the case for any empty sections, or any sections not found in the file, like the "recommendation" section we misspelled above.
- Yep, mixing dashes and asterisks. Some people just want to watch the world burn.

# Summary
Ok, now you're pushing it with the summaries. Same as before, it will either be merged with the other two summary sections or cause a failure.

# Description
Yep, this works too.

---
Now say that these lines are not meant to be part of this Description section. You had the best intentions, even adding that horizontal line separator.

Unfortunately, as far as the script is concerned, a section only ends when another section begins (with a new header), or when end of file is reached.

So if you want to have some content at the end of the file that is not related to a SysReptor section, you'll have to put it inside one last heading.
