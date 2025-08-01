use leetcode_rs::ListNode;
use leetcode_rs::vec_to_listnode;

pub struct Solution;

impl Solution {
    // Add two numbers.
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        let mut result = vec![];
        let mut carry = 0;

        let mut x = l1;
        let mut y = l2;
        while x.is_some() || y.is_some() {
            let a = x.as_ref().map(|x| x.val).unwrap_or(0);
            let b = y.as_ref().map(|x| x.val).unwrap_or(0);
            let r = Self::_add(a, b, &mut carry);
            result.push(r);

            x = x.and_then(|x| x.next);
            y = y.and_then(|x| x.next);
            // log::info!("x={x:?}, y={y:?}");
        }
        if carry > 0 {
            result.push(carry);
        }

        vec_to_listnode(result)
    }

    fn _add(a: i32, b: i32, carry: &mut i32) -> i32 {
        let mut c = *carry + a + b;
        *carry = c / 10;
        c %= 10;
        log::info!("carry={carry} a={a} b={b} c={c}.");
        c
    }
}

fn test(a: Vec<i32>, b: Vec<i32>, expected: Vec<i32>) {
    assert_eq!(
        vec_to_listnode(expected),
        Solution::add_two_numbers(vec_to_listnode(a), vec_to_listnode(b)),
    );
}

fn main() {
    env_logger::init();
    test(vec![2, 4, 3], vec![5, 6, 4], vec![7, 0, 8]);
    test(vec![0], vec![0], vec![0]);
    test(vec![9; 7], vec![9; 4], vec![8, 9, 9, 9, 0, 0, 0, 1]);
}
