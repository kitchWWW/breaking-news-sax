import random
import os

def doAndSay(com):
	print(com)
	os.system(com)

def pan(name,l,r):
	doAndSay("sox tmp/"+name+".wav tmp/"+name+"_pl.wav norm "+l)
	doAndSay("sox tmp/"+name+".wav tmp/"+name+"_pr.wav norm "+r)
	doAndSay("sox -M -c 1 tmp/"+name+"_pl.wav -c 1 tmp/"+name+"_pr.wav tmp/"+name+"_po.wav ")
	doAndSay("rm tmp/"+name+"_pr.wav tmp/"+name+"_pl.wav")

def doForFile(fileName):
	doAndSay("rm tmp/*")
	doAndSay("ffmpeg  -i uploads/"+fileName+"_in.ogg tmp/in.wav")

	doAndSay("sox tmp/in.wav tmp/1.wav trim 0 0:04.5 norm -1")
	doAndSay("sox tmp/in.wav tmp/2.wav trim 0:05 0:10 norm -1 fade 0.1 -0 0.1")
	doAndSay("sox tmp/in.wav tmp/3.wav trim 0:15 0:03 norm -1 fade 0.1 -0 0.1")

	doAndSay("sox tmp/3.wav tmp/3r.wav reverse tempo 0.1 pad 5 pitch -1200")
	pan("3r","-5","-5")
	pan("3","-1","-1")


	doAndSay("sox tmp/2.wav tmp/snippet1.wav trim 0:03 0:01 norm -1 tempo 0.1 fade 0.1 -0 0.1")
	doAndSay("sox tmp/snippet1.wav tmp/snippet2.wav tempo 0.333 pad 15")
	pan("snippet2","-5","-5")

	arr = list(range(8))

	for i in arr:
		doAndSay("sox tmp/2.wav tmp/cut"+str(i+1)+".wav trim 0:0"+str(i+1)+" 0:01 fade 0.1 -0 0.1 pitch "+str(random.randint(-1200, 1200)))

	for i in arr:
		doAndSay("sox tmp/cut"+str(i+1)+".wav tmp/cut"+str(i+1)+"r.wav reverse pitch "+str(random.randint(-200, 200)))

	for i in arr:
		panOptions = [["-100","-1"],["-1","-100"],["-5","-3"],["-3","-5"],["-4","-4"],["-7","-2"],["-2","-7"]]
		panSettings = random.choice(panOptions)
		pan("cut"+(str(i+1)),panSettings[0],panSettings[1])
		panSettings = random.choice(panOptions)
		pan("cut"+(str(i+1))+"r",panSettings[0],panSettings[1])

	arr3 = []
	for i in range(8):
		arr3.append(str(i+1)+"r")
		arr3.append(""+str(i+1))
	random.shuffle(arr3)

	print(arr3)
	mystr = "sox "
	for i in arr3:
		mystr += " tmp/cut"+i+"_po.wav "

	mystr +=" tmp/shuffle_po.wav pad 25"
	doAndSay(mystr)

	doAndSay("sox tmp/2.wav tmp/2r1.wav reverse pad 5.1")
	doAndSay("sox tmp/2.wav tmp/2r2.wav reverse pad 5.2")

	pan("2r1","-100","-1")
	pan("2r2","-1","-100")

	doAndSay("sox tmp/1.wav tmp/1a.wav trim 0.5 0:04")
	doAndSay("sox tmp/1a.wav tmp/1b.wav fade 0.01 -0 0.01")

	doAndSay("sox tmp/1b.wav tmp/drone1.wav rate tempo 0.1")
	doAndSay("sox tmp/1b.wav tmp/drone2.wav rate tempo 0.1 pitch -1200 reverse pad 1")
	doAndSay("sox tmp/1b.wav tmp/drone3.wav rate tempo 0.1 pitch -500 reverse pad 2")
	doAndSay("sox tmp/1b.wav tmp/drone4.wav rate tempo 0.1 pitch -800 reverse pad 5")
	doAndSay("sox tmp/1b.wav tmp/drone5.wav rate tempo 0.1 pitch -2400 reverse pad 7")

	pan("drone1","-3","-1")
	pan("drone2","-1","-3")
	pan("drone3","-10","-1")
	pan("drone4","-1","-10")
	pan("drone5","-3","-3")

	doAndSay("sox -m tmp/snippet2_po.wav tmp/3r_po.wav tmp/shuffle_po.wav  tmp/2r1_po.wav tmp/2r2_po.wav tmp/drone1_po.wav tmp/drone2_po.wav tmp/drone3_po.wav tmp/drone4_po.wav tmp/drone5_po.wav tmp/mostOut.wav norm -1 trim 0 0:50 fade 0.1 -0 0.1")

	splitSpot = random.randint(25,40)
	
	doAndSay("sox tmp/mostOut.wav tmp/mostOut1.wav trim 0 0:"+str(splitSpot)+" fade 0.01 -0 0.01")
	doAndSay("sox tmp/mostOut.wav tmp/mostOut2.wav trim 0:"+str(splitSpot)+" 0:50 fade 0.01 -0 0.01")
	doAndSay("sox tmp/mostOut1.wav tmp/3_po.wav tmp/mostOut2.wav tmp/z_allout.wav")
	doAndSay("cp tmp/z_allout.wav uploads/"+fileName+"_out.wav")



