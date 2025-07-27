pub struct Solution;

impl Solution {
    pub fn merge_sorted_array(nums1: &mut Vec<i32>, m: i32, nums2: &mut Vec<i32>, n: i32) {
        let mut idx = 0;

        while idx < nums1.len() - 1 {
            let a = nums1[idx];
            let b = nums1[idx + 1];
            eprintln!("idx={idx} a={a} b={b}");

            // find slice that is inside nums2 and drain it.
            let j = nums2.partition_point(|&x| x <= b);
            if j < nums2.len() {
                for x in nums2.drain(0..j) {
                    if x < a {
                        nums1.insert(idx, x);
                    } else {
                        nums1.insert(idx + 1, x);
                    }
                    idx += 1;
                    eprintln!("handing x={x} when a={a}, b={b}, nums1={nums1:?} idx={idx}");
                }
            }
            idx += 1;
        }

        // append leftover from nums2 to nums1
        nums1.splice(idx.., nums2);
    }
}

fn main() {
    let inst = std::time::Instant::now();

    let mut nums1 = vec![1, 2, 3, 0, 0, 0];
    let mut nums2 = vec![2, 5, 6];
    Solution::merge_sorted_array(&mut nums1, 3, &mut nums2, 3);
    assert_eq!(nums1, vec![1, 2, 2, 3, 5, 6]);

    println!("=======");
    nums1 = vec![1];
    nums2 = vec![];
    Solution::merge_sorted_array(&mut nums1, 1, &mut nums2, 0);
    assert_eq!(nums1, vec![1]);

    println!("=======");
    nums1 = vec![0];
    nums2 = vec![1];
    Solution::merge_sorted_array(&mut nums1, 0, &mut nums2, 1);
    assert_eq!(nums1, vec![0, 1]);
    println!("Took {:?}", inst.elapsed());
}
