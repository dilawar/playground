#include <algorithm>
#include <cassert>
#include <chrono>
#include <functional>
#include <iostream>
#include <map>

using std::cout;
using std::endl;

class LRUCache {
public:
  LRUCache(int capacity) : capacity(capacity), pCache({}) {}

  int get(int key) {
    std::cout << "get '" << key << "' " <<  " cache size=" << pCache.size() << std::endl;
    if (auto found = pCache.find(key); found != pCache.end()) {
      cout << " found it: " << found->second.second << endl;
      return found->second.second;
    }
    return -1;
  }

  void put(int key, int value) {
    // todo: check capacity and eviction
    if (pCache.size() >= capacity) {
      // printf("eviction");
      // find the least recently used key
      std::vector<std::pair<long, int>> new_vec;
      new_vec.reserve(capacity);
      
      // transform 
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

  friend std::ostream &operator<<(std::ostream &os, LRUCache const &obj) {
    os << "[";
    for(auto i: obj.pCache)
    {
      os << i.first << "=" << i.second.second << ",";
    }
    os << "]" << endl;
    return os;
  }

private:
  int capacity;
  std::map<int, std::pair<long, int>> pCache;
};


int main(int argc, char const *argv[]) {
  // Your LRUCache object will be instantiated and called as such:
  LRUCache *obj = new LRUCache(2);
  obj->put(1, 1);
  cout << *obj << endl;
  obj->put(2, 2);
  cout << *obj << endl;
  obj->get(1);
  cout << *obj << endl;
  obj->put(3, 3);
  cout << *obj << endl;
  obj->get(2);
  cout << *obj << endl;
  obj->put(4, 4);
  cout << *obj << endl;
  obj->get(1);
  cout << *obj << endl;
  obj->get(3);
  cout << *obj << endl;
  obj->get(4);
  cout << *obj << endl;
}
