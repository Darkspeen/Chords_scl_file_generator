import math
import os

flag = True

def to_ratio(s):
    if (s.split(':')[0] != ''):
        p = s.split(':')[0]
        q = s.split(':')[1]
    elif (s.split('/')[0] != ''):
        p = s.split('/')[0]
        q = s.split('/')[1]
    else:
        print("Invalid ratio")
        return 0
    return int(p) / int(q)


def cent_dif(f1, f2):
    return 1200 * (math.log2(f1/f2))


def fileWrite(n, des, arr, fun, tuning):
    c = tuning * (2 ** ((-9 + fun) / 12))
    f = open(n, "w+", encoding="utf-8")
    f.write(f"!\t{n}\n!\n{des}\n\t{len(arr)}\n!\n")
    for i in range(0, len(arr)):
        aux = arr[i]
        f.write(f"\t{'{0:.5f}'.format(cent_dif(aux, c))}\n")
    f.close()
    print("\n\nSCL File created")

if __name__ == "__main__":
    while (flag):
        tun = 440
        a = 9
        notes = ['C ', 'C#', 'D ', 'D#', 'E ', 'F ', 'F#', 'G ', 'G#', 'A ', 'A#', 'B ']
        fundamental = int(input("Pitch class of the fundamental: "))
        interval = int(input("Pitch class of the interval: "))
        ratio = input("Ratio for interval: ")
        r = to_ratio(ratio)
        rtn_cnts = input("Retune by any cents? [y/n]: ")
        if (rtn_cnts == 'y'):
            retune_cents = int(input("How many cents?: "))
        else:
            retune_cents = 0
        tun = tun*(2**(retune_cents/1200))

        if (interval - a > 0):
            i = (interval - a) % 12
        else:
            i = (interval - a) + 12
        interval -= fundamental
        if (interval < 0):
            interval += 12
        if (fundamental - a > 0):
            f = (fundamental - a) % 12
        else:
            f = fundamental - a
        freq1 = tun * (2 ** (f / 12))
        if(fundamental != 0):
            freq2 = tun * (2 ** (i / 12))*(1/r)
        else: freq2 = freq1*(2**(interval/12))*(1/r)

        # cents = math.ceil(cents(freq1, freq2))
        cents = cent_dif(freq2, freq1)
        print(f"Cents of difference between fundamental {'{0:.5f}'.format(freq1)} Hz TET and {'{0:.5f}'.format(freq2)} Hz JI: >>> {'{0:.5f}'.format(abs(cents))} cents")
        if(cents > 0):
            print(f">>> Retuned by +{round(cents)} cents <<<")
        else: print(f">>> Retuned by {round(cents)} cents <<<")
        retune = input("\nShow retuning? [y/n]: ")
        if (retune == 'y'):
            nfrq = freq2
            aux = input("\nChord in pitch class form: ")
            acordes = []
            for j in aux:
                if (j == 'T'):
                    j = 10
                elif (j == 'E'):
                    j = 11
                else:
                    j = int(j)
                acordes.append(j)
            rat = []
            ratf = []
            rat.append('1:1')
            ratf.append(1)
            print(f"Ratio for {notes[(acordes[0]+fundamental)%12]}: {rat[0]}")
            for j in range(1, len(acordes)):
                if(acordes[j] == interval):
                    aux = print(f"Ratio for {notes[(acordes[j]+fundamental)%12]}: {ratio}")
                    rat.append(ratio)
                    ratf.append(to_ratio(ratio))
                else:
                    aux = input(f"Ratio for {notes[(acordes[j] + fundamental) % 12]}: ")
                    rat.append(aux)
                    ratf.append(to_ratio(aux))
            retuned = []
            for j in range(0, len(acordes)):
                    retuned.append(ratf[j] * nfrq)

            print("\n#############################################################")
            print("###                      Retuning                         ###")
            print("#############################################################\n")
            ctr = 0
            for j in acordes:
                aux = (fundamental + j)%12
                print(f"Tuning for {notes[aux]}: {'{0:.5f}'.format(retuned[ctr])} Hz\n")
                ctr += 1

            fil = input("Create file? [y/n]:")
            if (fil == 'y'):
                nam = input("Name of chord?: ")
                fname = nam + "--"
                if (cents < 0):
                    fname += f"minus{str(abs(round(cents)))}.scl"
                else:
                    fname += f"plus{str(abs(round(cents)))}.scl"
                desc = f"{nam} chord with ratios "
                for j in rat[1:]:
                    desc += f"{j},"
                desc = desc.rstrip(desc[-1])
                filearray = []
                counter = 0
                for j in range(0, 12):
                    if (len(acordes) != 0):
                        if(acordes[0] == j):
                            filearray.append(float(retuned[0]))
                            retuned.pop(0)
                            acordes.pop(0)
                        else:
                            filearray.append(tun * (2 ** (-9 / 12)))
                    else:
                        filearray.append(tun * (2 ** (-9 / 12)))
                fileWrite(fname, desc, filearray, fundamental, tun)
                filearray.clear()
            rat.clear()
            ratf.clear()
        os.system("CLS")
        inp = input("Continue? [y/n]: ")
        if (inp == 'n'):
            flag = False
        os.system("CLS")

####################################################################
# 					    	 Notes  	    					   #
####################################################################

# 	notas = ['C ', 'C#', 'D ', 'D#', 'E ', 'F ', 'F#', 'G ', 'G#', 'A ', 'A#', 'B ']
#             0      1    2     3     4     5      6    7     8     9     T     E

####################################################################
# 						Intervals Ratios						   #
####################################################################
# NOTE:
#      for 1200 * log_2(f_TET/f_ratio)
#      if cents < 0 --> f_ratio > f_TET by x cents
#      else f_ratio < f_TET  by x cents
# ----------------------------------------------------------------------------------
# >>>>>>> 1J
#               ~1/3 tone ≈ {11:10}

# >>>>>>> 2m ≈ {18:17, 16:15, 15:14}
#               ~^2/3 tone ≈ {25:24, 13:12}

# >>>>>>> 2M ≈ {10:9, 9:8}
#               ~2M+1/3 tone ≈ {8:7}
#               ~2M+1/4 tone ≈ {12:11, 15:13}
#               ~2M+2/3 tone ≈ {7:6}

# >>>>>>> 3m ≈ {13:11, 6:5}
#               ~3m+~1/4 tone ≈ {11:9, 16:13}

# >>>>>>> 3M ≈ {5:4, 14:11}
#               ~3M+1/3 tone ≈ {9:7}
#               ~3M+1/4 tone ≈ {13:10}
# >>>>>>> 4J ≈ {4:3}
#               ~4J+1/3 tone ≈ {15:11, [49:36]}
#               ~4J+1/4 tone ≈ {11:8}
#               ~4J+2/3 tone ≈ {25:18}

# >>>>>>> 4A ≈ {[[169:121], 7:5, 45:32, [55:39, 140:99], 64:45, 10:7, [63:44, 242:169]}
#               ~4A+1/3 tone ≈ {36:25, 13:9}
#               ~4A+1/4 tone ≈ {[132:91], 16:11}72:49
#               ~4A+2/3 tone ≈ {[72:49]}

# >>>>>>> 5J ≈ {3:2}

# >>>>>>> 6m ≈ {11:7, 8:5}
#               ~6m+1/4 tone ≈ {13:8}

# >>>>>>> 6M ≈ {5:3}
#               ~6M+1/3 tone ≈ {12:7}

# >>>>>>> 7m ≈ {7:4, 16:9, 9:5}
#               ~7m+~1/4 tone ≈ {11:6, 13:7}

# >>>>>>> 7M ≈ {28:15, 15:8, 17:9}
#               ~7M+~1/3 tone ≈ {48:25}

####################################################################
# 							Chords								   #
####################################################################
# M    = 047
# m    = 037
# V7   = 047T
# dis  = 036
# Aum  = 048
# M7   = 047E
# m7   = 037T
# 7o   = 0369
# m7b5 = 036T
# +2 just add 2 after closest small number
# +4 just add 5 after closest small number