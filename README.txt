Welcome to the EasyChair slide generator. This is a simple script to
support physical PC meetings for EasyChair-supported conferences and
workshops. It has been used successfully for at least ISSTA 2008,
ISSTA 2010, ISSTA 2011, ESEC/FSE 2011, ISSTA 2013, ISSTA 2014, and
FSE 2014.

Here's how to use it:

0. This script assumes a Unix machine (Linux, MacOS X, ...) with
   LaTeX installed.

1. Use EasyChair 'Administration -> Other Utilities -> List of
   Reviews' to download the textual list of reviews; store it as
   "Inputs/reviews.txt".

2. Anonymize reviewers and subreviewers for papers that have conflict
   with some chair; you can replace names with "Reviewer 1",
   "Reviewer 2", etc.

3. Use a spreadsheet to prepare the discussion list, and then export
   it into a text file "Inputs/order.txt" where easy line had this
   format:

   Paper number<TAB>Discussion lead<TAB>Paper title and authors

   (The last field is unused and there for the PC chairs' convenience
   only. It can be safely omitted.)

4. Place in "Inputs/reviewers.txt" the list of reviewers, using names
   separated by spaces and "_" between first and last name (e.g.,
   John_Doe).

5. In directory "Templates", suitably edit "header.tex". Edit
   "footer.tex" and "slide.tex" if you want to personalize them as
   well, although that is optional.

6. Run "make clean" (to be safe), then run "make".

7. If everything works as expected, all you need should be in
   directory "Outputs":

   - Meeting slides: file "presentation.pdf"
   - Discussion lists for the PC members: directory "DiscussionLists"
   - Seating assignments: file "seating.txt" (if the search based
     algorithm is successful in avoiding having reviewers of a paper
     sit besides a colleague with a conflict on that same paper. At
     the top of the file, there is information on the number of
     conflicts that could not be solved).

* Notes:

  There are some sample input file that you can use to test the tool
  in your environment. Simply run "make" in the directory where this
  README is and check that the expected outputs are generated in the
  "Outputs" directory. If not, you will have adjust your environment
  and/or the script (hopefully the former).

  In case of LaTeX problems with some Unicode characters in author
  names or paper titles (e.g., 'é') at Step 6, the workaround is to
  manually replace some characters with ASCII (e.g.., 'e').

  See the Makefile for other possible useful features (e.g.,"make
  questions" after this to create the discussion lists where "?"
  identifies papers with chair conflicts

* Acknowledgements:

  See the comments at the beginning of the "generate_slides" script
  for details on the creator of and contributors for this tool.

This work is licensed under a Creative Commons Attribution 3.0
Unported License - http://creativecommons.org/licenses/by/3.0/
