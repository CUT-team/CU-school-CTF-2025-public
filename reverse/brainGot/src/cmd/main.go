package main

import (
	"bufio"
	"context"
	crand "crypto/rand"
	_ "embed"
	"encoding/binary"
	"fmt"
	mrand "math/rand"
	"os"
	"strings"

	"github.com/tetratelabs/wazero"
	"github.com/tetratelabs/wazero/api"
	wasi "github.com/tetratelabs/wazero/imports/wasi_snapshot_preview1"
)

var (
	heapOffset uint32 = 4096
	//go:embed wasm/brainrot.wasm
	brainrotWASM []byte
)

func brainrotExecute(ctx context.Context, mod api.Module, input string) (string, error) {
	mem := mod.Memory()
	if mem == nil {
		return "", fmt.Errorf("no memory found 😭")
	}

	inputBytes := []byte(input)
	inputPtr := heapOffset
	heapOffset += uint32(len(inputBytes))
	heapOffset += uint32(len(inputBytes))
	if ok := mem.Write(inputPtr, inputBytes); !ok {
		return "", fmt.Errorf("no memory 💀")
	}

	brainrotate := mod.ExportedFunction("brainrotate")
	if brainrotate == nil {
		return "", fmt.Errorf("no brainrot found 😭")
	}

	result, err := brainrotate.Call(ctx, uint64(inputPtr), uint64(len(inputBytes)))
	if err != nil {
		// return fmt.Errorf("brainrotate.Call: %v", err)
		return "", fmt.Errorf("brainrotate failed 😳")
	}

	outPtr := uint32(result[0] & 0xFFFFFFFF)
	outLength := uint32(result[0] >> 32)

	outBytes, ok := mem.Read(outPtr, outLength)
	if !ok {
		return "", fmt.Errorf("can't read memory 😭")
	}

	return string(outBytes), nil
}

func getUniqueBytes(input string) []byte {
	uniqueBytes := make(map[byte]struct{})
	var result []byte

	for _, r := range input {
		runeBytes := []byte(string(r))

		if len(runeBytes) == 0 {
			continue
		}

		firstByte := runeBytes[0]
		if _, exists := uniqueBytes[firstByte]; !exists {
			uniqueBytes[firstByte] = struct{}{}
			result = append(result, firstByte)
		}
	}
	return result
}

var (
	BrainrotKey         = "tralalero🦈tralala"
	brainrotUniqueBytes = getUniqueBytes(BrainrotKey)
	brainrotUniqueLen   = len(brainrotUniqueBytes)
)

func initiateBrainrot(ctx context.Context, mod api.Module, seed uint64, input string) (string, error) {
	rand := mrand.New(mrand.NewSource(int64(seed)))

	var brainrotAnimals = []string{
		"bombardiro🐊✈️crocodilo",
		"bombombini🦢✈️gusini",
		"ballerina☕🩰cappuccina",
		"tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁tung🪵🥁sahur",
		"brrr🐒🌲patapim",
		"lirili🌵🐘larila",
		"trippi🦐🐱troppi",
		"trulimero🎩🎭trulicina",
		"capuccino☠️🍶assassino",
		"glorbo🍍🐊fruttodrillo",
		"frulli🍓🌀frulla",
	}

	gameSize := len(input)
	if gameSize%10 != 0 {
		gameSize += 10 - (gameSize % 10)
	}
	var animalsInGame = make([]string, 0, gameSize)

	for range gameSize {
		animalIndex := rand.Intn(len(brainrotAnimals))
		animalsInGame = append(animalsInGame, brainrotAnimals[animalIndex])
	}

	var out strings.Builder
	for i, s := range animalsInGame {
		var inputChar byte
		if i <= len(input)-1 {
			inputChar = input[i]
		}
		randChar := brainrotUniqueBytes[rand.Intn(brainrotUniqueLen)]
		brainrotInput := string(inputChar) + string(randChar) + s
		brainrotOut, err := brainrotExecute(ctx, mod, brainrotInput)
		if err != nil {
			return "", fmt.Errorf("bruh")
		}
		// println("->", brainrotOut) // DEBUG only
		out.WriteString(brainrotOut)
	}
	return out.String(), nil
}

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("Usage: %s <flag>\n", os.Args[0])
		os.Exit(1)
	}

	ctx := context.Background()
	r := wazero.NewRuntime(ctx)
	defer r.Close(ctx)

	_, err := r.NewHostModuleBuilder("env").
		NewFunctionBuilder().
		WithFunc(func(ctx context.Context, m api.Module, size uint32) uint32 {
			ptr := heapOffset
			heapOffset += size
			return ptr
		}).
		Export("malloc").
		Instantiate(ctx)
	if err != nil {
		panic(err)
	}

	if _, err = wasi.Instantiate(ctx, r); err != nil {
		panic(err)
	}

	mod, err := r.InstantiateWithConfig(ctx, brainrotWASM,
		wazero.NewModuleConfig().WithStartFunctions("_initialize"))
	if err != nil {
		panic(err)
	}

	var seed uint64
	if err := binary.Read(crand.Reader, binary.LittleEndian,
		&seed); err != nil {
		panic(err)
	}
	fmt.Println(seed)

	brainrotOut, err := initiateBrainrot(ctx, mod, seed, os.Args[1])
	if err != nil {
		panic(err)
	}

	file, err := os.OpenFile("brainrot.txt", os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0644)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	_, err = writer.WriteString(brainrotOut)
	if err != nil {
		panic(err)
	}

	if err = writer.Flush(); err != nil {
		panic(err)
	}
}
