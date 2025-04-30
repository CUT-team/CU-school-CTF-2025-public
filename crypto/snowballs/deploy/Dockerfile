FROM gcc:latest

WORKDIR /app

COPY ./app /app

RUN g++ -std=c++17 -o server server.cpp
RUN g++ -std=c++17 -o snow_1.0 snow_1.0.cpp 

ENTRYPOINT ["./server"]