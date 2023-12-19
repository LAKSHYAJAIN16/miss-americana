def colour_creator(acoustic, dance, energy, tempo, valence):
    # Define the types
    types = [
        "sad energy",
        "happy energy",
        "sad no_energy",
        "happy no_energy"
    ]
    
    type_to_pallete = {
        "happy energy" : [
            "ffbe0b",
            "fb5607",
            "ff006e",
            "8338ec",
            "3a86ff"
        ],
        "sad energy" : [
            "5f0f40",
            "9a031e",
            "fb8b24",
            "e36414",
            "0f4c5c"    
        ],
        "happy no_energy" : [
          "995d81",
          "eb8258",
          "f6f740",
          "d8dc6a",
          "7192be"  
        ],
        "sad no_energy" : [
            "595959",
            "7f7f7f",
            "a5a5a5",
            "cccccc",
            "f2f2f2"
        ],
    }
    # Define weight
    weight = 0
    colors = []
    type = ""
    
    if energy >= 0.5:
        if valence >= 0.5:
            # Incredibly Happy song
            type = "happy energy"
            weight = dance * 2 * (tempo / 100)
        else:
            # Sad song but energy
            type = "sad energy"
            weight = dance * (tempo / 100) * acoustic
    else:
        if valence >= 0.5:
            # Happy song but no energy
            type = "happy no_energy"
            weight = dance * 2 * (tempo / 100)
        else:
            # Sad song but no energy
            type = "sad no_energy"
            weight = dance * (tempo / 100) * acoustic
            
    return [type_to_pallete[type], weight, type]