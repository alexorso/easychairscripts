Welcome to the EasyChair slide generator.  This is a simple script to support physical PC meetings for EasyChair-supported conferences and workshops.  It has been used successfully for at least ISSTA 2008, ISSTA 2010, ISSTA 2011, ESEC/FSE 2011, ISSTA 2013, and ISSTA 2014.

Here's how to use it:

0. This script assumes a Unix machine (Linux, MacOS X, ...) with LaTeX installed.

1. Use EasyChair 'Administration -> Other Utilities -> List of Reviews' to download the textual list of reviews; store it as "reviews.txt"
1.1. Anonymize reviewers and subreviewers for papers that have conflict with some chair; you can replace names with "Reviewer 1", "Reviewer 2", etc.
1.2. In 2014, we used a spreadsheet to prepare the discussion list, and then exported it into a text file "order.txt" where easy line had this format:
Paper number<TAB>Discussion lead<TAB>Conflicts separated by comma<TAB>PC paper or not<TAB>Paper authors and title
1.3. Using "order.txt" we could skip steps 2 and 3.

2. Set up discussion leaders.  Either:
2a. Edit "reviews.txt" and add a line "DISCUSSION LEADER: <discussion leader name>" the line after "PRELIMINARY DECISION"
2b. Or: Set up a file "leaders.txt" in the format "Paper number<TAB>Reviewer".

3. Place in "papers.txt" the list of papers to be discussed (paper numbers separated by whitespace).  (You may wish to generate "papers.txt" out of some annotated working file, as you may have to change the order from time to time. The enclosed 'Makefile' uses 'papers-full.txt' as a source for that.)

4. Place in "reviewers.txt" the list of reviewers (names separated by spaces and "_" between first and last name--e.g., Alex_Orso)

5. Suitably edit header.tex, footer.tex, and slide.tex.

6. Run 'python generate_slides.py'.
6.1. This may create LaTeX problems with some Unicode characters in author names or paper titles (e.g. 'é'); the workaround was to manually replace some characters with ASCII (e.g. 'e').

7. The resulting slides will be in "presentation.pdf", and the discussion lists for the PC members in directory "DiscussionLists"
7.1. In 2014, we also ran "make questions" after this to create the discussion lists where "?" identifies papers with chair conflicts

8. The script will also output a possible seating order on standard output, avoiding having reviewers of a paper sit besides a colleague with a conflict on that same paper.

Note: You can run the tool in this directory to see how the script works.  It should produce the files as described above.  If not, adjust your environment and/or the script.

Enjoy! - Andreas, Kim, and Alex

Written by 
* Andreas Zeller <zeller@cs.uni-saarland.de> (contact),
* Kim Herzig <kim@cs.uni-saarland.de>, and
* Alex Orso <orso@cc.gatech.edu>

This work is licensed under a Creative Commons Attribution 3.0 Unported License - http://creativecommons.org/licenses/by/3.0/
