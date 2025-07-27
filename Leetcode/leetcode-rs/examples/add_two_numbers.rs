use leetcode_rs::ListNode;
use leetcode_rs::linkedlist_to_list;
use leetcode_rs::list_to_linkedlist;
use std::collections::LinkedList;

pub struct Solution;

impl Solution {
    // Add two numbers.
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        let mut l1 = list_to_linkedlist(l1);
        let mut l2 = list_to_linkedlist(l2);

        let mut result = LinkedList::new();

        let mut carry = 0;

        while l1.front().is_some() || l2.front().is_some() {
            let a = l1.pop_front().unwrap_or(0);
            let b = l2.pop_front().unwrap_or(0);
            let r = Self::_add(a, b, &mut carry);
            log::debug!("\t a={a:?} b={b:?} r={r}.");
            result.push_back(r);
        }
        if carry > 0 {
            result.push_back(carry);
        }
        log::info!("result={result:?}");
        linkedlist_to_list(result)
    }

    fn _add(a: i32, b: i32, carry: &mut i32) -> i32 {
        let mut c = *carry + a + b;
        *carry = c / 10;
        c = c % 10;
        log::info!("carry={carry} a={a} b={b} c={c}.");
        c
    }
}

fn test(a: Vec<i32>, b: Vec<i32>, expected: Vec<i32>) {
    let a = LinkedList::from_iter(a.into_iter());
    let b = LinkedList::from_iter(b.into_iter());
    assert_eq!(
        linkedlist_to_list(LinkedList::from_iter(expected.into_iter())),
        Solution::add_two_numbers(linkedlist_to_list(a), linkedlist_to_list(b)),
    );
}

fn main() {
    env_logger::init();
    test(vec![2, 4, 3], vec![5, 6, 4], vec![7, 0, 8]);
    test(vec![0], vec![0], vec![0]);
    test(vec![9; 7], vec![9; 4], vec![8, 9, 9, 9, 0, 0, 0, 1]);
    test(vec![2, 4, 3], vec![5, 6, 4], vec![7, 0, 8]);
}
