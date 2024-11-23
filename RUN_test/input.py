exec(open("Modified_data/realtime.py").read()) # enable realtime and sim control panel
trick.stop(20.0)

#==================================
# Start the variable server client.
#==================================
varServerPort = trick.var_server_get_port();
CannonDisplay_path = os.environ['HOME'] + "/trick_sims/sim_skydiver/skydiver_display_server.py"
if (os.path.isfile(CannonDisplay_path)) :
    CannonDisplay_cmd = CannonDisplay_path + " " + str(varServerPort) + " &" ;
    print(CannonDisplay_cmd)
    os.system( CannonDisplay_cmd);
else :
    print('Oops! Can\'t find ' + CannonDisplay_path )