#An example input file for multimesa.py

#run command is python multimesa.py example.py

#Location to write out folders too
output_folder="output/"

#Name to call inlist that get written if not set defaults to inlist_cluster
inlist_name='inlist_cluster'

folder_num=1
# if set to 1 we number the folders otherwise use the var names


#Defaults assume varaibles are linearly looped and that the name of varaible is the mesa one.
mass_min=1.0
mass_max=10.0
mass_range=3
mass_name="initial_mass"
mass_type="linear"
mass_section='control'

z_list=[0.01,0.02,0.03]
z_name="initial_z"
z_section='control'

