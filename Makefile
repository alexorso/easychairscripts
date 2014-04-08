
presentations.pdf:	papers.txt
	python ./generate_slides.py # -search
	# Adding "-search" uses a searchSeat() method which uses a simple simulated annealing algorithm to optimise conflicts in seat plan generation.

clean:
	rm -fr presentation.*
	rm -fr reviews
	rm -fr DiscussionLists
	rm -f papers.txt papers-full.txt leaders.txt

papers.txt:	papers-full.txt
	grep '^[1-9]' papers-full.txt | awk '{ print $$1 }' > papers.txt

papers-full.txt:	order.txt
	<order.txt cut -f1,5 >papers-full.txt
	<order.txt cut -f-2 >leaders.txt

stats:	presentations.pdf
	grep -c ^D DiscussionLists/*.txt
	grep -c ^R DiscussionLists/*.txt

# Add question marks for papers where one of the chairs has a conflict
# so the reviewers know they could be 'D' or 'R', but the chairs don't know
questions:	presentations.pdf
	mkdir questions
	cp DiscussionList/*.txt questions
	cd questions
	# replace XYZ, ABC (and add more if needed) with the numbers of papers that have conflict with chairs
	for x in *; do sed -i -e 's/^ XYZ\t/?XYZ\t/' -e 's/^ ABC\t/?ABC\t/' $x; done
	# quick and dirty way to shorten text; you may want smaller font and/or landscape printing
	for x in *txt; do sed 's/^\(.*\)\t\(......................................................................\)....*$/\1\t\2.../' $x | enscript -B -p a.ps; ps2pdf a.ps ${x/txt/pdf}; rm a.ps; done

# Identify orderings in which a reviewer has to deal with two papers in a row
# Also identify orderings in which a reviewer has to deal with a paper right after a conflict, which can be bad
distcheck:	presentations.pdf
	for file in DiscussionLists/*.txt; do \
	echo $$file; \
	awk '{ print $$1 }' $$file | tr '\012' ' ' | grep -E '(R|D)[0-9]* (R|D)[0-9]*'; \
	grep -A1 ^C $$file | grep -E 'txt-(R|D)'; \
	done