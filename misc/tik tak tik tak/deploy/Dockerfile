FROM golang:alpine as builder

WORKDIR /app

COPY . .

RUN go build -o morse-tcp-server cmd/tiktak/main.go

FROM alpine

WORKDIR /app

COPY --from=builder /app/morse-tcp-server .

EXPOSE 8080

ENTRYPOINT ["/app/morse-tcp-server"]
