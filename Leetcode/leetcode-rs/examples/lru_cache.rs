use std::collections::HashMap;

///
///  - book-keeping: access time (steady clock, multi threaded).
///  - least recently used (order is needed.)
///
struct LRUCache {
    capacity: usize,
    key_vals: HashMap<i32, i32>,
    key_access_times: HashMap<i32, usize>,
    counter: usize,
}

/**
 * `&self` means the method takes an immutable reference.
 * If you need a mutable reference, change it to `&mut self` instead.
 */
impl LRUCache {
    fn new(capacity: i32) -> Self {
        // pick a stack-only hashmap
        Self {
            capacity: capacity as usize,
            key_vals: HashMap::with_capacity(capacity as usize),
            key_access_times: HashMap::with_capacity(capacity as usize),
            counter: 0,
        }
    }

    fn get(&mut self, key: i32) -> i32 {
        let val = self.key_vals.get(&key).clone();
        if val.is_none() {
            return -1;
        }
        let v = *val.unwrap();
        self.update_access_time(key);
        v
    }

    fn put(&mut self, key: i32, value: i32) {
        // println!("put {key}={value}: capacity: {}, size: {}", self.capacity, self.key_vals.len());
        if self.key_vals.contains_key(&key) {
            self.update_access_time(key);
            self.key_vals.insert(key, value);
            return;
        }

        if (self.key_vals.len() >= self.capacity) {
            // find lru key (find min by value, O(n))
            let mut min_value = usize::MAX;
            let mut min_key = -1;
            for (k, v) in self.key_access_times.iter() {
                if *v < min_value {
                    min_value = *v;
                    min_key = *k;
                }
            }

            // lru key
            // println!("evicting {min_key} {:?}", self.key_vals);
            self.key_vals.remove(&min_key);
            self.key_access_times.remove(&min_key);
        }

        self.key_vals.insert(key, value);
        self.update_access_time(key);

        assert!(self.key_vals.len() <= self.key_vals.capacity());
    }

    #[inline]
    fn update_access_time(&mut self, key: i32) {
        // let now = Instant::now();
        self.counter += 1;
        self.key_access_times.insert(key, self.counter);
        // printl//////////n!("|atime| {key}={now:?}");
    }
}

fn main() {
    env_logger::init();
    let obj = LRUCache::new(3);
    obj.put(1, 1);
    obj.put(2, 2);
}
