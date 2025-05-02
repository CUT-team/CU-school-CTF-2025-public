package main

import (
	"fmt"
	"os"
)

/*
	this code is epic >.<
	mfw I forgor what it does: +_+
	mb I should include C++ library ot smth ?_?
	cuz I heard that C++ is fun to shoot your leg :D
	but I'm too lazy to fight with C++ tho :[
	yeah I'm crazy >:)
*/

type NumsContext struct {
	num int
	bit bool
}

func printnc(nc NumsContext) {
	fmt.Println(nc)
}

const (
	u        = "u"
	U        = "U"
	C        = "C"
	g        = "g"
	a        = "a"
	CU       = C + U
	ga       = g + a
	uCU      = u + CU
	CUCU     = CU + CU
	CUCUCU   = CU + CU + CU
	CUCUCUCU = CU + CU + CU + CU
	CUga     = CU + ga
)

type SignerHolder struct {
	secret   string
	SignChan chan int
	DataChan chan string
}

func NewSignerHolder(secret string) *SignerHolder {
	return &SignerHolder{
		secret:   secret,
		SignChan: make(chan int),
		DataChan: make(chan string),
	}
}

func main() {
	signSecret := u + CU + CUCU + CUga
	signerHolder := NewSignerHolder(signSecret)

	// robots
	var (
		sadRobot    = ":["
		killerRobot = ">:x"
		funnyRobot  = ":D"
		coolRobot   = "B)"
	)

	// clown faces
	var (
		happyClownFace     = ":+>" // a happy face with a nose and mouth
		holyClownFace      = "O:+>"
		starryClownFace    = "*+>" // starry eyed look
		sleepyClownFace    = "|+>" // wanna sleep
		eyeClosedClownFace = "T+>" // look he is shy
		magicClownFace     = "=+>" // he looking kinda magic +_+
		sadReversedFace    = ">+:"
		sadFace            = ":+<"
	)

	sus := "ඞ" // <<<<<< THIS is SUS!!!!!
	susChan := make(chan string, 999999)
	susChan <- sus // I love it :]

	var (
		leetNumber         = 1337
		answerToLifeNumber = 42
		piNumber           = 314
		badNumber          = 0xBAD
		coffeeNumber       = 0xC0FFEE
		deadBeefNumber     = 0xDEADBEEF
		spookyNumber       = 666
		luckyNumber        = 777
		passwordNumber     = 12345
		funnyNumber        = 69
	)

	bool2int := func(b bool) int {
		var i int
		if b {
			i = 1
		}
		return i
	}

	some := NumsContext{
		bit: leetNumber > coffeeNumber,
		num: leetNumber - bool2int(deadBeefNumber > luckyNumber) + funnyNumber,
	}

	printnc(NumsContext{
		bit: piNumber > badNumber,
		num: spookyNumber - bool2int(answerToLifeNumber > piNumber),
	})

	printnc(NumsContext{
		bit: passwordNumber+passwordNumber > spookyNumber-spookyNumber,
		num: bool2int(badNumber > answerToLifeNumber),
	})

	printnc(NumsContext{
		num: leetNumber + 0x1337,
		bit: holyClownFace > magicClownFace,
	})

	printnc(NumsContext{
		bit: coffeeNumber-funnyNumber > passwordNumber,
		num: 13 + 37, // <<<<<<<< this for some reason looks sus too tho
	})
	signerHolder.DataChan <- (<- susChan) // + did I already said how I love it >:]
	// hey you sussy baka fr fr >:)

	println(happyClownFace) // happy > sad, change my mind +_+
	// or nah idk +_o
	fmt.Println(">+:" == sadReversedFace) // oh it is sad
	println(sadReversedFace + sadFace + sadReversedFace + sadFace + sadReversedFace) // sad now :((
	fmt.Println(">:x" + killerRobot + killerRobot + killerRobot) // ok now killer robots
	fmt.Print("??? :?> ballin or smth (+_+) (+_+) ")
	fmt.Printf("ok = %T\n", some)
	println("console> ")
	sussy := "sus" + "sus" + "sus" + "sus" + "sus" + "sus" + "sus"

	var input string
	fmt.Scanln(&input)

	if input != "1337 > 69 +++++++++++" {
		println(sussy)
		os.Exit(funnyNumber)
	}
	println("yay :> :> :>" + funnyRobot + coolRobot + "+++++++++++++++++") // wait where is sus :[

	susChan <- "amogus" // haha here it is

	cArt := `
+--{ RSA 2048 }---+
|                 |
|                 |
|    ,-:::::      |
| <;;;''   \      |
| |||             |
| $$$             |
|  88bo,__,o,     |
|  "YUMMMMMP"     |
|                 |
+_-_-_-_-_-_-_-_-++`

	susChan <- cArt

	println("is sus", -(-(-leetNumber)) < +deadBeefNumber)

	susChan <- "U" // kinda-sad-looking cat :<
	susChan <- "C"

	num := - answerToLifeNumber - passwordNumber
	println("<+> hacking in progress", num)

	println(bool2int(len(starryClownFace) > len(sadRobot)) > bool2int(len(eyeClosedClownFace) > len(sleepyClownFace)))
	println(bool2int(bool2int(len(magicClownFace) > spookyNumber) > bool2int(len(coolRobot) > spookyNumber)) > -69) // hehe funny number :]

	println("<+: <-----<") // haha reversed happy clown face pointed with arrow

	uArt := `
+++{ RSA 2048 }++++
|                 |
|    :::    :+:   |
|    <;     ;;;   |
|   ||'     |||   |
|   $$      $$$   |
|   88     d888   |
|    "YmmMMMM""   |
|                 |
|                 |
+_-_-__-__-__-__-_+`

	susChan <- uArt
	println("-------", num < answerToLifeNumber)
	println("+++++++++")
	susChan <- cArt
	println("-----")

	data := "3i<@>BBI>>IqY>#>S1>JD^.N4<<)<p< >oe>qN>>>Q"
	for _, b := range data {
		signerHolder.DataChan <- string(b) // +rep
	}
	susChan <- string('C' - 'U')
	susChan <- string('U' - 'C')

	println("-------------")
	println("ok <+:")
	println("++++++++++++++++++")

	susChan <- "CU"
	println("----------------------")
	
	println(">.< o.o >.<")
	fmt.Println("ok >_>")
	fmt.Print("------")
	fmt.Print("> >.< <") // idk what this is now lol

	println("<<<< e-p-i-c-_-g-a-m-e-r >>>>")
	println(">_> <_< <_< >_> >_> >_+ +_+ +_+ +_+ :+)") // my fav emotions order. remember that!
}
