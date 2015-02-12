#An example input file for multimesa.py

#run command is python multimesa.py example2.py

#Location to write out folders too
output_folder="output/"

# if set to 1 we number the folders otherwise use the _name value
folder_num=1


#Defaults assume varaibles are linearly looped and that the name of varaible is the mesa one.
#Assumes varaibles exist inside control_inlist unless specified as star 
mass_list=[7.0,8.0,9.0]
mass_name="initial_mass"
mass_section="control"

var_list=[0.00001,0.0001,0.001]
var_name="varcontrol_target"
var_section="control"

mesh_list=[0.1,0.5,1.0]
mesh_name="mesh_delta_coeff"
mesh_section="control"


rot_list=[0.0,0.25,0.5]
rot_name="new_omega_div_omega_crit"
rot_section="star"
