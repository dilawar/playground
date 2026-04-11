#include <atomic>
#include <iostream>
#include <mutex>
#include <set>
#include <thread>

std::atomic<int> x(0), y(0);
std::mutex result_mutex;
std::set<std::pair<int, int>> results;

void run_once() {
  x.store(0, std::memory_order_relaxed);
  y.store(0, std::memory_order_relaxed);

  int r1, r2;

  std::thread A([&]() {
    r1 = y.load(std::memory_order_acquire);
    x.store(1, std::memory_order_relaxed);
  });

  std::thread B([&]() {
    r2 = x.load(std::memory_order_relaxed);
    y.store(1, std::memory_order_release);
  });

  A.join();
  B.join();

  std::lock_guard<std::mutex> lock(result_mutex);
  results.insert({r1, r2});
}

int main() {
  const int ITERATIONS = 100000;

  for (int i = 0; i < ITERATIONS; i++) {
    if (i % 1000 == 0) {
      std::cout << i << "/" << ITERATIONS << ": seen ";
      for (auto e : results) {
        std::cout << "{" << e.first << ", " << e.second << "}, ";
      }
      std::cout << std::endl;
    }
    run_once();
  }

  std::cout << "Observed outcomes after " << ITERATIONS << " runs:\n";
  for (auto &[r1, r2] : results) {
    std::cout << "  r1=" << r1 << ", r2=" << r2 << "\n";
  }

  std::cout << "\nNot observed:\n";
  std::set<std::pair<int, int>> all = {{0, 0}, {0, 1}, {1, 0}, {1, 1}};
  for (auto &p : all) {
    if (results.find(p) == results.end()) {
      std::cout << "  r1=" << p.first << ", r2=" << p.second << "\n";
    }
  }

  return 0;
}
