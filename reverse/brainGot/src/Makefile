LOCAL_BIN:=$(CURDIR)/bin
PATH:=$(PATH):$(LOCAL_BIN)

PKG:=brainrot
MAIN_ENTRYPOINT:=./cmd/
WASM_ENTRYPOINT:=./cmd/wasm/
MAIN_BIN:=$(LOCAL_BIN)/brainrot
WASM_BIN:=./cmd/wasm/brainrot.wasm

ifneq (,$(wildcard .env))
	include .env
	export
endif

.PHONY: .app-deps
.app-deps:
	go mod tidy

.PHONY: install
install: .app-deps

.PHONY: run
run:
	@go run $(MAIN_ENTRYPOINT) $(FLAG)

.PHONY: build
build:
	@mkdir -p $(LOCAL_BIN)
	tinygo build \
		-buildmode=c-shared -target=wasip1 \
		-o $(WASM_BIN) $(WASM_ENTRYPOINT)
	GOOS=$(GOOS) GOARCH=$(GOARCH) go build \
		-ldflags="-s -w" \
		-trimpath -buildvcs=false \
		-o $(MAIN_BIN) $(MAIN_ENTRYPOINT)

.PHONY: clean
clean:
	rm -ri $(LOCAL_BIN)/*
