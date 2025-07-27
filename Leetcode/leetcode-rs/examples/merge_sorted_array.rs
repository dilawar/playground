pub struct Solution;

impl Solution {
    pub fn merge_sorted_array(nums1: &mut Vec<i32>, m: i32, nums2: &mut Vec<i32>, n: i32) {
        nums1.drain(m as usize..);
        nums1.reserve((m + n) as usize);
        let mut idx = 0;

        // eprintln!("111 nums1={nums1:?}, nums2={nums2:?}.");
        while !nums1.is_empty() && idx < nums1.len() {
            let a = nums1[idx];

            // Any element from second vector which is less than a goes before a.
            let j = nums2.partition_point(|&x| x <= a);
            for x in nums2.drain(0..j) {
                nums1.insert(idx, x);
                idx += 1;
            }
            // eprintln!("handing when a={a}, nums1={nums1:?} idx={idx}");

            if nums1.get(idx + 1).is_none() {
                break;
            }

            let b = nums1[idx + 1];
            // find slice that is inside nums2 and drain it.
            let j = nums2.partition_point(|&x| x <= b);
            // eprintln!("idx={idx} j={j} a={a} b={b}");
            if j < nums2.len() {
                for x in nums2.drain(0..j) {
                    nums1.insert(idx + 1, x);
                    idx += 1;
                    // eprintln!("handing x={x} when a={a}, b={b}, nums1={nums1:?} idx={idx}");
                }
            }

            idx += 1;
        }

        // append leftover from nums2 to nums1
        nums1.extend(nums2.iter());
    }
}

fn main() {
    let inst = std::time::Instant::now();

    println!("0. =======");
    let mut nums1 = vec![4, 5, 6, 0, 0, 0];
    let mut nums2 = vec![1, 2, 3];
    Solution::merge_sorted_array(&mut nums1, 3, &mut nums2, 3);
    assert_eq!(nums1, vec![1, 2, 3, 4, 5, 6]);

    println!("1. =======");
    let mut nums1 = vec![1, 2, 3, 0, 0, 0];
    let mut nums2 = vec![2, 5, 6];
    Solution::merge_sorted_array(&mut nums1, 3, &mut nums2, 3);
    assert_eq!(nums1, vec![1, 2, 2, 3, 5, 6]);

    println!("2. =======");
    nums1 = vec![2, 0];
    nums2 = vec![1];
    Solution::merge_sorted_array(&mut nums1, 1, &mut nums2, 1);
    assert_eq!(nums1, vec![1, 2]);

    println!("3. =======");
    nums1 = vec![1];
    nums2 = vec![];
    Solution::merge_sorted_array(&mut nums1, 1, &mut nums2, 0);
    assert_eq!(nums1, vec![1]);

    println!("4. =======");
    nums1 = vec![0];
    nums2 = vec![1];
    Solution::merge_sorted_array(&mut nums1, 0, &mut nums2, 1);
    assert_eq!(nums1, vec![1]);

    println!("Took {:?}", inst.elapsed());
}
