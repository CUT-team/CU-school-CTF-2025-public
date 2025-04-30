//go:build wasm && wasip1
// +build wasm,wasip1

package main

import (
	"strings"
	"unsafe"
)

var BrainrotKey = "tralalero🦈tralala"

//go:wasmexport brainrotate
func brainrotate(ptr, size uint32) uint64 {
	input := ptrToString(ptr, size)

	const (
		emojiStartPoint = 0x1F600
		asciiStartPoint = 0x30
		asciiEndPoint   = 0x7E
	)

	var out strings.Builder
	allowedRange := asciiEndPoint - asciiStartPoint + 1

	for i := range input {
		b := input[i] ^ BrainrotKey[i%len(BrainrotKey)]
		mapped := int(b) % allowedRange
		emojiRune := rune(emojiStartPoint + mapped)
		out.WriteRune(emojiRune)
	}

	outBytes := []byte(out.String())
	outPtr := malloc(uint32(len(outBytes)))
	if outPtr == 0 {
		return 0
	}

	outSlice := unsafe.Slice((*byte)(unsafe.Pointer(uintptr(outPtr))), len(outBytes))
	copy(outSlice, outBytes)
	return uint64(outPtr) | uint64(len(outBytes))<<32
}

//go:wasmimport env malloc
func malloc(size uint32) uint32

func ptrToString(ptr uint32, size uint32) string {
	return unsafe.String((*byte)(unsafe.Pointer(uintptr(ptr))), size)
}

func main() {}
