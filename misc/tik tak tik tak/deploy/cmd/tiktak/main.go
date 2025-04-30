package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"net"
	"os"
	"strings"
	"time"
)

var flag = os.Getenv("FLAG")
var port = os.Getenv("PORT")
var morseFlag = ""

var randomMessages = []string{
	"Hey, how's it going?",
	"Did you see the latest update?",
	"Just checking in...",
	"Let me think about that...",
	"Brb, need to grab coffee.",
	"LOL, that's hilarious!",
	"Wait, what do you mean?",
	"I'll get back to you soon.",
	"Interesting point!",
	"Hold on a sec...",
	"Can you repeat that?",
	"Okay, I'm back.",
	"Let's discuss this later.",
	"Sorry, I was AFK.",
	"Got it, thanks!",
	"Are you still there?",
	"Give me a moment...",
	"Almost done...",
	"Let me check...",
	"Yep, that works!",
	"Not sure about that.",
	"Maybe in a bit.",
	"Just a little longer...",
	"Almost there...",
	"Let's wrap this up.",
	"One sec...",
	"Thinking...",
	"Interesting...",
	"Gotcha!",
	"Alright, moving on.",
}

func init() {
	flag = strings.ToUpper(flag)

	morseCode := map[rune]string{
		'A': ".-", 'B': "-...", 'C': "-.-.", 'D': "-..", 'E': ".", 'F': "..-.",
		'G': "--.", 'H': "....", 'I': "..", 'J': ".---", 'K': "-.-", 'L': ".-..",
		'M': "--", 'N': "-.", 'O': "---", 'P': ".--.", 'Q': "--.-", 'R': ".-.",
		'S': "...", 'T': "-", 'U': "..-", 'V': "...-", 'W': ".--", 'X': "-..-",
		'Y': "-.--", 'Z': "--..",
		'0': "-----", '1': ".----", '2': "..---", '3': "...--", '4': "....-",
		'5': ".....", '6': "-....", '7': "--...", '8': "---..", '9': "----.",
		'{': "-.--.", '}': "-.--.-", '_': "..--.-",
	}

	for _, c := range flag {
		if code, ok := morseCode[c]; ok {
			morseFlag += code + " "
		} else {
			morseFlag += string(c) + " "
		}
	}
}

func sendRandomMessage(conn net.Conn) {
	msg := randomMessages[rand.Intn(len(randomMessages))]
	conn.Write([]byte("Server: " + msg + "\n"))
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	fmt.Printf("New connection from %s\n", conn.RemoteAddr())

	reader := bufio.NewReader(conn)
	conn.Write([]byte("=== Welcome to the Chat Server! ===\n"))
	conn.Write([]byte("Type anything and press Enter to continue...\n\n"))

	for _, symbol := range morseFlag {
		// conn.Write([]byte("(waiting for your input...)\n"))
		_, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("Connection error: %v\n", err)
			return
		}

		switch symbol {
		case '.':
			sendRandomMessage(conn)
			time.Sleep(250 * time.Millisecond)
		case '-':
			sendRandomMessage(conn)
			time.Sleep(500 * time.Millisecond)
		case ' ':
			sendRandomMessage(conn)
			time.Sleep(1 * time.Second)
		}
	}

	conn.Write([]byte("\n=== End of conversation ===\n"))
}

func main() {
	rand.Seed(time.Now().UnixNano())
	if port == "" {
		port = ":8080"
	}
	listener, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()

	fmt.Println("Interactive Morse TCP Server is running on " + port)
	fmt.Printf("Flag: %s (Morse: %s)\n", flag, morseFlag)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}
		go handleConnection(conn)
	}
}
