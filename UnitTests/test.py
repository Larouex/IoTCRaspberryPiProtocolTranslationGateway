import ../gateway
#explorepy.set_bt_interface('pybluez')
explore = explorepy.Explore()
explore.connect(device_name='Explore_143A')
explore.set_channels(15)
explore.visualize(bp_freq=(1, 40), notch_freq=50)+

    short_options = "hv"
    long_options = ["help", "verify"]
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        #sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verify"):
            print ("Verificatioon mode...")
            #reg_id = "d-001"
            #symmetric_key = ""
            #sas = SymmetricKey(logging.getLogger())
            config = Config(logging.getLogger())
            dpscache = DpsCache(logging.getLogger())
            nanoblesenseservices = NanoBLESenseServices(logging.getLogger())
            #asymmetric_key = sas.compute_derived_symmetric_key(reg_id, symmetric_key)
            #print(asymmetric_key)
            #print(config.data)
            #print(dpscache.data)
            #print(nanoblesenseservices.data)

            #print("Connecting...")
            #global peripheral
            #peripheral = btle.Peripheral("C7:94:90:1C:8F:3C")
