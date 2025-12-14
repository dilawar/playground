#include <algorithm>
#include <cassert>
#include <chrono>
#include <functional>
#include <ios>
#include <iostream>
#include <map>

class LRUCache {
public:
  LRUCache(int capacity) : capacity(capacity), pCache({}) {}

  int get(int key) {
    std::cout << " pCache size: " << pCache.size() << std::endl;
    if (auto found = pCache.find(key) != pCache.end()) {
      return pCache[key].second;
    }
    return -1;
  }

  void put(int key, int value) {
    // todo: check capacity and eviction
    if (pCache.size() >= capacity) {
      printf("eviction");
      // find the least recently used key
      std::vector<std::pair<long, int>> new_vec = {};
      std::transform(pCache.cbegin(), pCache.cend(), new_vec.begin(),
                     [](auto const &x) -> std::pair<long, int> {
                       return {x.second.first, x.first};
                     });
      
      make_heap(new_vec.begin(), new_vec.end(),
                            std::greater<std::pair<long, int>>());

      auto lru_elem = new_vec[0];
      // erase the key
      pCache.erase(lru_elem.second);
    }

    auto now = std::chrono::steady_clock::now().time_since_epoch().count();
    // check
    pCache[key] = std::make_pair(now, value);
  }

private:
  int capacity;
  std::map<int, std::pair<long, int>> pCache;
};

int main(int argc, char const *argv[]) {
  // Your LRUCache object will be instantiated and called as such:
  LRUCache *obj = new LRUCache(10);
  auto param_1 = obj->get(10);
  assert(param_1 == -1);
  obj->put(10, 9);
  param_1 = obj->get(10);
  assert(param_1 == 9);
}
