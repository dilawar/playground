pub struct Solution;

impl Solution {
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        let mut x: Vec<(i32, usize)> = nums.into_iter().enumerate().map(|(i, v)| (v, i)).collect();
        x.sort_unstable();
        for i in 0..x.len() {
            let a = x[i].0;
            let b = target - a;
            if let Ok(j) = x.binary_search_by(|probe| probe.0.cmp(&b)) {
                eprintln!("x[{i}]={a} x[{j}]={b}");
                return vec![x[i].1 as i32, x[j].1 as i32];
            }
        }
        vec![]
    }
    pub fn two_sum_n2(nums: Vec<i32>, target: i32) -> Vec<i32> {
        for i in 0..nums.len() {
            for j in i + 1..nums.len() {
                if target == nums[i] + nums[j] {
                    return vec![i as i32, j as i32];
                }
            }
        }
        vec![]
    }
}

fn main() {
    env_logger::init();
    assert_eq!(Solution::two_sum(vec![2, 7, 11, 15], 9), vec![0, 1]);
    assert_eq!(Solution::two_sum(vec![3, 2, 4], 6), vec![1, 2]);
    assert_eq!(Solution::two_sum(vec![3, 3], 6), vec![0, 1]);
}
