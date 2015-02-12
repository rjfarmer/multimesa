#Copyright (c) 2015, Robert Farmer rjfarmer@asu.edu

#Permission to use, copy, modify, and/or distribute this software for any
#purpose with or without fee is hereby granted, provided that the above
#copyright notice and this permission notice appear in all copies.

#THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


#This is desgined to read in a file that specifies a series of options
#These options are then iterated over to create a series of mesa inlists
#in different folders.
#Thus creating an easy way to create lots of mesa models
from __future__ import print_function
import numpy as np
import getopt
import sys as sys
import itertools
import shutil as s
import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

opts, extra = getopt.getopt(sys.argv[1:],'')

#Input varaibles
input_file=extra[0]

try:
	e=__import__(input_file.replace(".py",''))
except IOError:
	print("File doesnt exist ",input_file)
	sys.exit(1)
except SyntaxError:
	raise

try:
	output_folder=e.output_folder
except AttributeError:
	print("No output_folder set")
	sys.exit(1)	

#Access the different avraibles we want to loop over
mesa_name=[]
mesa_loop=[]
mesa_sec=[]
short_name=[]
for i in e.__dict__:
	if i[-5:] == "_name":
		short_name.append(i[:-5])
		mesa_name.append(getattr(e,short_name[-1]+"_name"))
		try:
			minX=getattr(e,short_name[-1]+"_min")
			maxX=getattr(e,short_name[-1]+"_max")
			useRng=True
			try:
				rngX=getattr(e,short_name[-1]+"_range")
			except AttributeError:
				useRng=False
				rngX=1
			try:
				spaceX=getattr(e,short_name[-1]+"_step")
			except AttributeError:
				spaceX=1
			try:
				typ=getattr(e,short_name[-1]+"_type")
			except AttributeError:
				typ='linear'	
			if typ=='log':
				minX=np.log10(minX)
				maxX=np.log10(maxX)
			elif typ=='linear':
				minX=minX
				maxX=maxX
			else:
				print("Invalid loop type either linear or log or set name_list",typ)
				sys.exit(1)
			
			if useRng:
				mesa_loop.append(np.linspace(minX,maxX,rngX))
			else:
				mesa_loop.append(np.arange(minX,maxX,spaceX))
		except AttributeError:
			try:
				mesa_loop.append(getattr(e,short_name[-1]+"_list"))
			except AttributeError:
				try:
					mesa_loop.append([getattr(e,short_name[-1]+"_value")])
				except:
					print("Bad name", short_name[-1])
					sys.exit(0)
		try:
			mesa_sec.append(getattr(e,short_name[-1]+"_section"))
		except AttributeError:
			mesa_sec.append("control")

#Now to make the inlists
k=1
for l in itertools.product(*mesa_loop):
	if e.folder_num:
		name=str(k)
	else:
		name=[]
		#Dont include range=1 varaibles
		for i in range(len(mesa_name)):
			if len(mesa_loop[i])>1:
				name.append(mesa_name[i])
				name.append("_")
				name.append(l[i])
				name.append("_")
		name[-1]=''
		name=''.join(map(str, name))
	
	outF=os.path.join(output_folder,name)
	mkdir_p(outF)
	
	#get possible extra values
	extra=[]
	try:
		extraName,extraVal,extraSec=e.callback(short_name,l)
	except AttributeError:
		extraName=[]
		extraVal=[]
		extraSec=[]
		pass
	
	outName=mesa_name+extraName
	outVal=list(l)+extraVal
	outSec=mesa_sec+extraSec
	
	with open(os.path.join(outF,"inlist_cluster"),'w') as f:
		f.write("&star_job\n")
		for i in range(len(outName)):
			if outSec[i]=="star":		
				f.write(outName[i]+" = "+str(outVal[i])+"\n")
		f.write("/ ! end of star_job namelist\n")
		f.write("&controls\n")
		for i in range(len(outName)):
			if outSec[i]=="control":		
				f.write(outName[i]+" = "+str(outVal[i])+"\n")
		f.write("/ ! end of control_job namelist\n")
	print(k)
	k=k+1
					
