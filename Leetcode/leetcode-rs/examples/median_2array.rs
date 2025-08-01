pub struct Solution;

impl Solution {
    pub fn find_median_sorted_arrays(mut nums1: Vec<i32>, mut nums2: Vec<i32>) -> f64 {
        // eprintln!("0.0 {nums1:?}");
        // eprintln!("0.1 {nums2:?}");

        nums2.reserve_exact(nums1.len());
        let mut i1 = 0;
        while !nums2.is_empty() && i1 < nums1.len() {
            let b = nums1[i1];
            let i2 = nums2.partition_point(|&x| x <= b);
            nums1.splice(i1..i1, nums2.drain(0..i2));
            eprintln!(" {nums1:?}");
            i1 += i2 + 1;
            // skip all index that ==b.
        }

        // left-over must be added.
        nums1.extend(nums2);

        // do the median.
        eprintln!("Final array {nums1:?}");
        let m = nums1.len();

        let mut i = m / 2;
        let mut j = i;
        if m % 2 == 0 {
            i = i - 1;
            j = i + 1;
        }

        ((nums1[i] + nums1[j]) as f64) / 2.0
    }
}

fn main() {
    assert_eq!(
        Solution::find_median_sorted_arrays(vec![1, 3], vec![2]),
        2.0
    );
    assert_eq!(
        Solution::find_median_sorted_arrays(vec![1, 2], vec![3, 4]),
        2.5
    );
    assert_eq!(
        Solution::find_median_sorted_arrays(vec![1, 2], vec![0, 0]),
        0.5
    );
}
