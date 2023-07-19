import pickle

def write():
    slovar = {
            224: f"а",
            225: f"б",
            226: f"в",
            227: f"г",
            228: f"д",
            229: f"е",
            230: f"ж",
            231: f"з",
            232: f"и",
            233: f"й",
            234: f"к",
            235: f"л",
            236: f"м",
            237: f"н",
            238: f"о",
            239: f"п",
            240: f"р",
            241: f"с",
            242: f"т",
            243: f"у",
            244: f"ф",
            245: f"х",
            246: f"ц",
            247: f"ч",
            248: f"ш",
            249: f"щ",
            251: f"ы",
            252: f"ь",
            253: f"э",
            254: f"ю",
            255: f"я" }

    obj = pickle.dumps(slovar)
    f = open("example.bin", "wb")
    f.write(obj)
    f.close()

def read():
        f = open("example.bin", "rb")
        stuff = f.read()
        f.close()
        slovar = pickle.loads(stuff)
        print(slovar)

#write()
read()