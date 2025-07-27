pub struct Solution;

impl Solution {
    /// Given an integer array nums sorted in non-decreasing order,
    /// remove some duplicates in-place such that each unique element appears
    /// at most twice. The relative order of the elements should be kept the same.
    pub fn remove_duplicates(nums: &mut Vec<i32>) -> i32 {
        let mut removed = 0usize;

        let mut idx = 0usize;
        let mut N = nums.len();
        while idx < N {
            let a = nums[idx];

            // These are optimization to speed things up.
            if let Some(b) = nums.get(idx + 1) {
                if a != *b {
                    idx += 1;
                    continue;
                }
                if let Some(c) = nums.get(idx + 2) {
                    if a != *c && *b != *c {
                        idx += 2;
                        continue;
                    }
                }
            }

            // Remove more than two consecutive duplicates.
            let j = nums.partition_point(|&x| x <= a);
            eprintln!("idx={idx}, a={a}, N={N}, j={j}, {nums:?}");
            if (idx + 2) < j {
                nums.drain(idx + 2..j);
                removed += j - idx - 2;
                eprintln!("range {}..{j}, #removed={removed}", idx + 2);

                N = nums.len();
                idx += 2;
            } else {
                idx += 1;
            }
        }
        nums.len() as i32
    }
}

fn main() {
    let mut num = vec![1, 1, 1];
    assert_eq!(Solution::remove_duplicates(&mut num), 2);
    assert_eq!(num, vec![1, 1]);

    println!("===========");
    num = vec![1, 2, 2, 2];
    assert_eq!(Solution::remove_duplicates(&mut num), 3);
    assert_eq!(num, vec![1, 2, 2]);

    println!("===========");
    num = vec![1, 1, 1, 2, 2, 3];
    assert_eq!(Solution::remove_duplicates(&mut num), 5);
    assert_eq!(num, vec![1, 1, 2, 2, 3]);

    println!("===========");
    num = vec![0, 0, 1, 1, 1, 1, 2, 3, 3];
    assert_eq!(Solution::remove_duplicates(&mut num), 7);
    assert_eq!(num, vec![0, 0, 1, 1, 2, 3, 3]);
}
