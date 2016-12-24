#An example input file for multimesa.py

#run command is python multimesa.py example3.py

#Location to write out folders too
output_folder="output/"

# if set to 1 we number the folders otherwise use the _name value
folder_num=1


#Defaults assume varaibles are linearly looped and that the name of varaible is the mesa one.
#Assumes varaibles exist inside control_inlist unless specified as star 
semi_list=[0.0,0.001,0.01,0.1]
semi_name="alpha_semiconvection"
semi_section="control"

over_list=[0.0,0.001,0.016,0.2]
over_name='overshoot_f_above_nonburn'
over_section='control'

thermo_list=[0.0,0.1,1.0,10.0]
thermo_name="thermo_haline_coeff"
thermo_section='control'

am_list=[0.0,0.5,1.0,1.5]
am_name="am_nu_factor"
am_section="control"




#This function is called once per iteration with the current set of parameters
#This then lets us set other parameters which may be dependant on the inputs 
#For instance lets say we have mass=8,9,10 and parameter y=1,2,3
#we could say when mass<9 set z=0.01 when mass>=9 set z=0.02 unless y <2 in which case z=0.0

#It should return 3 lists, where the lists are the mesa_name,value and section
#Note if you have set folder_num=0 this will not add these names to the output folder path

#If you dont care about this stuff just comment out the function, it doesn't need to exist

#Note names are the short name ie for mass_name='initial_mass', names='mass' not initial_mass
def callback(names,val):
	outName=[]
	outVal=[]
	outSec=[]
	
	semi=0
	over=0
	thermo=0
	am=0
	#Loops over both lists at the same time 
	for i,j in zip(names,val):
		if i=='semi':
			semi=float(j)
		if i=='over':
			over=float(j)
		if i=='thermo':
			thermo=float(j)
		if i=='am':
			am=float(j)

	if semi >0.0:
		outName.append('allow_semiconvective_mixing')
		outVal.append('.true.')
		outSec.append('control')
	else:
		outName.append('allow_semiconvective_mixing')
		outVal.append('.false.')
		outSec.append('control')
		
	if over >0.0:
		outName.append('overshoot_f_below_nonburn')
		outName.append('overshoot_f_above_burn_h')
		outName.append('overshoot_f_below_burn_h')
		outName.append('overshoot_f_above_burn_he')
		outName.append('overshoot_f_below_burn_he')
		outName.append('overshoot_f_above_burn_z')
		outName.append('overshoot_f_below_burn_z')
		a=[over]*7
		outVal=outVal+a
		a=['control']*7
		outSec=outSec+a

	if thermo >0.0:
		outName.append('allow_thermohaline_mixing')
		outVal.append('.true.')
		outSec.append('control')
	else:
		outName.append('allow_thermohaline_mixing')
		outVal.append('.false.')
		outSec.append('control')
		
		
	return outName,outVal,outSec
