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
            let j = nums.partition_point(|&x| x <= a);
            eprintln!("a={a}, N={N}, j={j}, {nums:?}");
            if j != nums.len() {
                // remove from idx+1 to j but only if more than two duplicates.
                if (idx + 2) < j {
                    nums.drain(idx + 2..j);
                    removed += j - idx - 2;
                    eprintln!(
                        " removing range {}..{j}, #removed={removed}\
                    .",
                        idx + 2
                    );

                    N = nums.len();
                    idx += 2;
                }
            }
            idx += 1;
        }
        nums.len() as i32
    }
}

fn main() {
    let mut num = vec![1, 1, 1, 2, 2, 3];
    assert_eq!(Solution::remove_duplicates(&mut num), 5);
    assert_eq!(num, vec![1, 1, 2, 2, 3]);

    num = vec![0, 0, 1, 1, 1, 1, 2, 3, 3];
    assert_eq!(Solution::remove_duplicates(&mut num), 7);
    assert_eq!(num, vec![0, 0, 1, 1, 2, 3, 3]);
}
