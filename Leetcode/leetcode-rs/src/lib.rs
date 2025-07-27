use std::collections::LinkedList;

pub struct Solution;

#[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}

pub fn list_to_linkedlist(l: Option<Box<ListNode>>) -> LinkedList<i32> {
    let mut result = LinkedList::new();
    let mut curr = l;
    while curr != None {
        let inner = curr.unwrap();
        result.push_back(inner.val);
        curr = inner.next;
    }

    result
}

pub fn linkedlist_to_list(mut ll: LinkedList<i32>) -> Option<Box<ListNode>> {
    let mut tail = None;
    while ll.front().is_some() {
        let v = *ll.front().unwrap();
        let node = ListNode { val: v, next: tail };
        tail = Some(Box::new(node));
        ll.pop_front();
    }

    tail
}
