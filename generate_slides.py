#!/usr/bin/env python
# encoding: utf-8
"""
generate_slides.py - EasyChair slide generator.  See 'README.txt' for details.

Created by Kim Herzig <kim@cs.uni-saarland.de> on 2008-03-14.
Edited by Andreas Zeller <zeller@cs.uni-saarland.de>.
Edited by Alex Orso <orso@cc.gatech.edu>.
Edited by Yue Jia <yue.jia@ucl.ac.uk> and Mark Harman <mark.harman@ucl.ac.uk>
Edited by Darko Marinov <marinov@illinois.edu>.

This work is licensed under a Creative Commons Attribution 3.0 
Unported License - http://creativecommons.org/licenses/by/3.0/
"""

import sys
import os
import math
import time
import re
from random import randrange,random
from math import exp

class Paper:
	def __init__(self, paper_number):
		self._number = paper_number
		self._content = ""
		self._authors = {}
		self._title = ""
		self._reviewers = {}
		self._leader = ""
		self._grades = {}
		self._conflicts = {}
			
	def setContent(self, content):
		self._content = content
#		print("PAPER " + self._number)
		
		lines = self._content.split("\n")
		authors = lines[0]
		authors = authors.replace(" and ",",")
		authors = authors.replace(", ",",")
		authors = authors[9:len(authors)]
		self._authors = authors.split(",")
		
		self._title = lines[1][7:len(lines[1])]

		for l in lines:
			if l.find("CONFLICT") > -1:
				conflict_line = l[23:len(l)]
				conflict_line = conflict_line.replace(", ",",")
				self._conflicts = conflict_line.split(",")
#				print(self._conflicts)
			if l.find("DISCUSSION") > -1:
				self._leader = l[19:len(l)]
#				print(self._leader)
		
		i = 0
		for l in lines:
			i = i + 1
			if l.find("SUMMARY OF REVIEWS") > 0:
				break

		r = 0
		leaderOK = 0
		while ((lines[i + r].strip() != "") and
		       (lines[i + r].find("+++") == -1)):
			review_parts = lines[i + r].strip().split(":")
			reviewer = review_parts[0].strip()

			# Strip co-reviewer
			if reviewer.find("(") >= 0:
				reviewer = reviewer[:reviewer.index("(")]
			
			grade = review_parts[1].strip()

			# Have colored grades
			g = int(grade.split()[0])
			if g > 0:
				grade = "\\textcolor{Green}{" + grade + "}"
			elif g < 0:
				grade = "\\textcolor{Red}{" + grade + "}"
			
			self._reviewers[r] = reviewer.strip()
			self._grades[r]	= grade

			r = r + 1

# xxx
# 			if reviewer.index(self._leader):
# 				leaderOK = 1

# 		if leaderOK == 0:
# 			print "Error: the leader is not one of the reviewers"
# 			exit

	def getNumber(self):
		return self._number
	
	def getAuthors(self):
		return self._authors

	def getContent(self):
		return self._content
			
	def getTitle(self):
		return self._title
				
	def getReviewers(self):
		return self._reviewers
					
	def getGrades(self):
		return self._grades
						
	def getConflicts(self):
		return self._conflicts

	def setLeader(self, leader):
		self._leader = leader

	def getLeader(self):
		return self._leader

class Presentation:
	def __init__(self):
		self._header = open("header.tex","r").read()
		self._footer = open("footer.tex","r").read()
		self._slide_xml = open("slide.tex","r").read()
		self._new_slides = ""
		self._num_slides = 0
	
	def createList(self,paper,reviewer,outfile):
		
		conf = 0
		for c in paper.getConflicts():
			c = c.replace(" ","_")
			# print "Comparing ", c, " and ", reviewer
			if c == reviewer:
				conf = 1

		rev = 0
		reviewers = paper.getReviewers()
		i = 0
		while i < len(reviewers):
			r = reviewers[i]
			r = r.replace(" ","_")
			# print "Comparing ", r, " and ", reviewer
			if r == reviewer:
				rev = 1
			i = i + 1

		lead = 0
		l = paper.getLeader()
		l = l.replace(" ","_")
		# print "Comparing ", l, " and ", reviewer
		if l == reviewer:
			lead = 1

		str = ""

		if conf == 1:
# 			print "C"
			str = "C\n"
		else:
			if lead == 1:
# 				print "D", paper.getNumber(), "\t", paper.getTitle()
				str = "%s%s%s%s%s" % ("D", paper.getNumber(), "\t", paper.getTitle(), "\n")
			else:
				if rev == 1:
# 					print "R", paper.getNumber(), "\t", paper.getTitle()
					str = "%s%s%s%s%s" % ("R", paper.getNumber(), "\t", paper.getTitle(), "\n")
				else:
# 					print " ", paper.getNumber(), "\t", paper.getTitle()
					str = "%s%s%s%s%s" % (" ", paper.getNumber(), "\t", paper.getTitle(), "\n")

		outfile.write(str)

	def addNewSlide(self,paper):
		
# 		print paper.getNumber(), "\t", paper.getTitle()
		
		new_slide_xml = self._slide_xml
		new_slide_xml = new_slide_xml.replace("NUMBER",paper.getNumber())
		new_slide_xml = new_slide_xml.replace("TITLE",paper.getTitle())
		
		authors_string = ""
		for a in paper.getAuthors():
			authors_string = authors_string + a + ", "
		authors_string = authors_string[0:len(authors_string)-2]
		new_slide_xml = new_slide_xml.replace("AUTHORS",authors_string)
		
		reviewers = paper.getReviewers()
		
		i = 0
		while i < len(reviewers):
			new_slide_xml = new_slide_xml.replace("REVIEWER\\_"+str(i+1),reviewers[i])
			new_slide_xml = new_slide_xml.replace("GRADE\\_"+str(i+1),paper.getGrades()[i])
			i = i + 1
		
		p = re.compile( 'REVIEWER\\\\_[1-9]')
		new_slide_xml = p.sub('',new_slide_xml)
		
		p = re.compile( 'GRADE\\\\_[1-9]')
		new_slide_xml = p.sub('',new_slide_xml)
		
		conflict_string = ""
		for c in paper.getConflicts():
			conflict_string = conflict_string + c + ", "

		conflict_string = conflict_string[0:len(conflict_string)-2]
		if conflict_string == "":
			conflict_string = "none"
		new_slide_xml = new_slide_xml.replace("CONFLICTS",conflict_string)

		new_slide_xml = new_slide_xml.replace("LEADER",paper.getLeader())
			
		self._new_slides = self._new_slides + "\n" + new_slide_xml

	def writePresentation(self):
		os.system("touch presentation.tex")
		new_presentation_file = open("presentation.tex","w")
		new_presentation_file.write(self._header)
		new_presentation_file.write(self._new_slides)
		new_presentation_file.write(self._footer)
		new_presentation_file.close()
		os.system("pdflatex presentation.tex")



def getOrder():
	papers_file = open("papers.txt")
	papers_content = papers_file.read()
	papers_file.close()
	return papers_content.split()

def getReviewers():
	reviewers_file = open("reviewers.txt")
	reviewers_content = reviewers_file.read()
	reviewers_file.close()
	return reviewers_content.split()
	
def getLeaders():
	leaders = {}
	leaders_file = open("leaders.txt")
	leaders_content = leaders_file.read()
	leaders_file.close()
	for line in leaders_content.split('\n'):
	    list = line.split('\t')
	    # print list
            if len(list) < 2:
		break
	    (paper, leader) = (list[0], list[1])
	    leader = leader.replace("_"," ")
	    leaders[paper] = leader
	    
	print leaders
	return leaders
	
def getPapers():
	review_file = open("reviews.txt","r")
	review_content = review_file.read()
	start_index = review_content.find("<pre>") + 5
	end_index = review_content.rfind("</div>")
	if(review_content.find("</pre>") != -1):
		end_index = min(end_index, review_content.find("</pre>"))
	review_content = review_content[start_index:end_index]

	# Some fixes - AZ
	review_content = review_content.replace("&nbsp;", " ")
	review_content = review_content.replace("&apos;", "'")

	papers = {}

	review_lines = review_content.split("\n")
	paper_content = ""
	paper_number = -1
	
	for line in review_lines:
		if(line.find("** PAPER") > 0 ):
			if(paper_number > -1):
				paper = papers[paper_number]
				paper.setContent(paper_content)
			i = line.find("** PAPER") + 8
			e = line.find("*",i)
			paper_number = line[i:e]
			paper_number = paper_number.strip()
			papers[paper_number] = Paper(paper_number)
			paper_content = ""
		else:
			paper_content = paper_content + line + "\n"
			
	if(paper_number > -1):
		papers[paper_number].setContent(paper_content)
		
	print len(papers)
	return papers

# Do a simple depth-first search on the graph of possible co-seatings
def findPath(seating_paths, reviewers, reviewers_seated = []):
	# print reviewers_seated
	
	if len(reviewers_seated) == len(reviewers):
		return reviewers_seated

	if len(reviewers_seated) > 0:
		last_reviewer = reviewers_seated[-1]
	else:
		last_reviewer = None

	for colleague in reviewers:
		if (last_reviewer is not None and 
			not seating_paths[last_reviewer].has_key(colleague)):
			continue  # Conflict with predecessor

		if colleague in reviewers_seated:
			continue  # Already seated
			
		tentative_reviewers_seated = reviewers_seated + [colleague]

		success = findPath(seating_paths, reviewers, tentative_reviewers_seated)
		if success is not None:
			return success

	return None
	
def generateSeating():
	# Reviewers A and B can sit side by side iff
	# - Reviewer A has not reviewed any paper with which reviewer B is in conflict
	# - Reviewer B has not reviewed any paper with which reviewer A is in conflict
	reviewers = getReviewers()
	papers = getPapers()

	seating_conflicts = {}
	numbers = papers.keys()
	numbers.sort()
	for paper_number in numbers:
		paper = papers[paper_number]
		for rev_a in paper.getReviewers().values():
			for rev_b in paper.getConflicts():
				if not seating_conflicts.has_key(rev_a):
					seating_conflicts[rev_a] = {}
				if not seating_conflicts.has_key(rev_b):
					seating_conflicts[rev_b] = {}
					
				# print "Seating conflict between", rev_a, "and", rev_b, "beacuse of paper", paper_number
					
				seating_conflicts[rev_a][rev_b] = paper_number
				seating_conflicts[rev_b][rev_a] = paper_number
	
	revs = []			
	for rev in getReviewers():
		rev = rev.replace('_', ' ')
		revs = revs + [rev]
		
	# Convert the conflicts into a positive graphs structure
	seating_paths = {}
	for rev_a in revs:
		for rev_b in revs:
			if (not seating_conflicts.has_key(rev_a) or 
		    	not seating_conflicts[rev_a].has_key(rev_b)):

				if not seating_paths.has_key(rev_a):
					seating_paths[rev_a] = {}
				if not seating_paths.has_key(rev_b):
					seating_paths[rev_b] = {}

				seating_paths[rev_a][rev_b] = 1
				seating_paths[rev_b][rev_a] = 1

	# Print the constraints
	# for rev_a in revs:
	# 	print "***", rev_a, "may sit besides",
	# 	if seating_conflicts.has_key(rev_a):
	# 		print
	# 	else:
	# 		print "anyone"
	# 		continue
	# 
	# 	for rev_b in revs:
	# 		if not seating_conflicts[rev_a].has_key(rev_b):
	# 			print "+", rev_b
	# 			
	# 	if seating_conflicts.has_key(rev_a):
	# 		print "**", rev_a, "may NOT sit besides"
	# 		for rev_b in revs:
	# 			if seating_conflicts[rev_a].has_key(rev_b):
	# 				print "-", rev_b, "because of paper", seating_conflicts[rev_a][rev_b]
					
	# Suggest a seating
	path = findPath(seating_paths, revs)
	print "*** Possible seating order:", path
					
		

def generateSlides():
	papers = getPapers()
	
	presentation = Presentation()
	
	paper_order = getOrder()
	
	leaders = getLeaders()
	for paper_number in leaders.keys():
	    papers[paper_number].setLeader(leaders[paper_number])
	
	# print(papers['11'])
	
	for p in paper_order:
		presentation.addNewSlide(papers[str(p.strip())])
		
        presentation.writePresentation()
        print "*** Slides generated in 'presentation.pdf'"

	reviewers = getReviewers()

	command = "%s %s" % ("rm -rf ", "DiscussionLists")
	os.system(command)
	command = "%s %s" % ("mkdir", "DiscussionLists")
	os.system(command)

	for r in reviewers:
		header = "%s%s%s" % ("*** List for ", r.replace("_", " "), " ***\n")
		filename = "%s%s%s" % ("DiscussionLists/", r, ".txt")

		# print "*** Generating list for", r.replace("_", " "), "in", filename, "***"

		command = "%s %s" % ("touch", filename)
		os.system(command)
		new_rev_file = open(filename,"w")
		new_rev_file.write(header)

		for p in paper_order:
# 			print p
# 			print papers[str(p.strip())]
			presentation.createList(papers[str(p.strip())], r, new_rev_file)

		new_rev_file.close()

	print "*** Individual discussion lists written to 'DiscussionLists/' subdirectory"
		
def splitPapers():
	papers = getPapers()
	
	os.system("mkdir reviews")
	
	for p in papers.values():
		f = open("reviews/review" + p.getNumber() + ".txt", 'w')
		f.write(p.getContent())
		f.close()
		
	print "*** Individual reviews written to 'reviews/' subdirectory"

# search seating plan ------

#Random swap two seats
def rand_swap_seats(seating_plan):
    new_seating_plan = seating_plan[:]
    i = randrange(len(new_seating_plan))
    j = randrange(len(new_seating_plan))
    
    new_seating_plan[i],new_seating_plan[j] = new_seating_plan[j],new_seating_plan[i]
    return new_seating_plan

# Conlict of Reviewer Seatings Fitness evaluation
def CR_fitness(seating_plan, seating_conflicts):
    fitness= 0;
    for i in range(len(seating_plan)-1):
        rev_a = seating_plan[i]
        rev_b = seating_plan[i+1]
        if not seating_conflicts.has_key(rev_a):
            continue
        if seating_conflicts[rev_a].has_key(rev_b):
            fitness = fitness + len(seating_conflicts[rev_a][rev_b])
    return  fitness

# Use simulated annealing search for seatings
def searchSeating():
    # generate confilct (using a list to store paper id in seating_conflicts)
    
    reviewers = []
    for rev in getReviewers():
        rev = rev.replace('_', ' ')
        reviewers = reviewers + [rev]
    
    papers = getPapers()
    
    seating_conflicts = {}
    numbers = papers.keys()
    numbers.sort()
    for paper_number in numbers:
        paper = papers[paper_number]
        for rev_a in paper.getReviewers().values():
            for rev_b in paper.getConflicts():
                if not seating_conflicts.has_key(rev_a):
                    seating_conflicts[rev_a] = {}
                if not seating_conflicts.has_key(rev_b):
                    seating_conflicts[rev_b] = {}
                
                if not seating_conflicts[rev_a].has_key(rev_b):
                    seating_conflicts[rev_a][rev_b]=[]
                if not seating_conflicts[rev_b].has_key(rev_a):
                    seating_conflicts[rev_b][rev_a]=[]
                seating_conflicts[rev_a][rev_b].append(paper_number)
                seating_conflicts[rev_b][rev_a].append(paper_number)
    # perform search
    seating_plan = reviewers[:]
    print str(CR_fitness(seating_plan, seating_conflicts))

    max_gen = 100000
    curr_gen = 0
    no_improvement = 0
    max_no_improvement = 1000
    bad_moves = 0;
    SearchSAInitTemp = 0.3
    SearchSACooling = 0.98
    SearchSACoolingSchedule = 100

    t = SearchSAInitTemp
    while curr_gen < max_gen:
        print "Gen " + str(curr_gen) + "| No. of conflicts: " + str(CR_fitness(seating_plan, seating_conflicts))
        new_seating_plan = rand_swap_seats(seating_plan)
        curr_fitness = CR_fitness(seating_plan, seating_conflicts)
        new_fitness = CR_fitness(new_seating_plan, seating_conflicts)
        #        print "Bad moves " + str(bad_moves) + " Temp: " + str(t)
        if exp(- (new_fitness - curr_fitness) / t) > random():
            if curr_fitness == new_seating_plan:
                no_improvement = no_improvement + 1
            else:
                no_improvement = 0
                if curr_fitness < new_seating_plan:
                    bad_moves = bad_moves + 1
            
            seating_plan = new_seating_plan

        else:
            no_improvement = no_improvement + 1




        if CR_fitness(new_seating_plan, seating_conflicts) == 0:
            print "Found solution at Gen  " + str(curr_gen) + "| No. of conflicts: " + str(CR_fitness(seating_plan, seating_conflicts))
            print seating_plan
            break
        if no_improvement > max_no_improvement:
            print "Failed! current solution at Gen  " + str(curr_gen) + "| No. of conflicts: " + str(CR_fitness(seating_plan, seating_conflicts))
            print seating_plan
            break
        if (curr_gen % SearchSACoolingSchedule == 0):
            t = t*SearchSACooling;
        
        curr_gen = curr_gen + 1



if __name__ == '__main__':
    splitPapers()
    generateSlides()
    print str(len(sys.argv))
    if len(sys.argv) > 1 and sys.argv[1] == "-search":
        searchSeating()
    else:
        generateSeating()
