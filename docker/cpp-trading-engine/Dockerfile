# Stage 1: Build static binary using Alpine
FROM alpine:3.21 AS builder
RUN apk add --no-cache g++ musl-dev
WORKDIR /app
COPY ../../src/cpp-trading-engine/main.cpp .
RUN g++ -O3 -std=c++17 -static -o trading-engine main.cpp
# Stage 2: Minimal scratch runtime
FROM scratch
WORKDIR /app
COPY --from=builder /app/trading-engine .
ENTRYPOINT ["./trading-engine"]