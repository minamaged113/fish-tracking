def get_beams_from_pingmode(pingmode):
    pingmode = int(pingmode)
    if (pingmode is 1 or pingmode is 2):
        return 48
    
    elif (pingmode is 3 or pingmode is 4 or pingmode is 5):
        return 96
    
    elif (pingmode is 6 or pingmode is 7 or pingmode is 8):
        return 64

    elif (pingmode is 9 or pingmode is 10 or pingmode is 11 or pingmode is 12):
        return 128
    
    else:
        return False
