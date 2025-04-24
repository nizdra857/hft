#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>

// Simulated "trade" processor
void processTrade(int id) {
    std::cout << "[TradeEngine] Processing trade ID: " << id << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // simulate some latency
}

int main() {
    std::srand(std::time(nullptr));
    std::cout << "[TradeEngine] Starting high-frequency trading engine..." << std::endl;

    int tradeId = 0;

    while (true) {
        int randDelay = std::rand() % 50 + 1; // simulate trade frequency
        std::this_thread::sleep_for(std::chrono::milliseconds(randDelay));
        processTrade(tradeId++);
    }

    return 0;
}
