use std::collections::VecDeque;
pub struct Solution;

impl Solution {
    pub fn my_atoi(s: String) -> i32 {
        let mut result = 0i64;

        // sanitize the string.
        let mut s = s.trim().as_bytes().iter();
        let mut is_neg = false;
        let mut digits: VecDeque<u8> = VecDeque::with_capacity(s.len());

        // first character is sign.
        if let Some(sign_byte) = s.next() {
            if *sign_byte == b'-' {
                is_neg = true;
            } else if *sign_byte == b'+' {
                is_neg = false;
            } else {
                let v = *sign_byte - b'0';
                if v <= 9 {
                    digits.push_back(v);
                } else {
                    // eprintln!("invalid digit or sign {sign_byte}");
                    return result as i32;
                }
            }
        }

        while let Some(c) = s.next() {
            if *c < b'0' || *c > b'9' {
                // eprintln!("{c} is not a valid digit...");
                break;
            }
            let v = *c - b'0';
            // eprintln!(" c={c} v={v} ");
            digits.push_back(v);
        }

        for (m, v) in digits.iter().rev().enumerate() {
            if *v == 0 {
                continue;
            }
            if m > 10 {
                result = i64::MAX;
                break;
            }
            result += (*v as i64) * 10_i64.pow(m as u32);
            // eprintln!(" v={v} m={m} result = {result}");
            if result > (i32::MAX as i64) {
                break;
            }
        }

        if is_neg {
            result = -result;
        }

        // eprintln!("\n=== result is {result}. Rounding...");
        if result > (i32::MAX as i64) {
            i32::MAX
        } else if result < (i32::MIN as i64) {
            i32::MIN
        } else {
            result as i32
        }
    }
}

fn main() {
    assert_eq!(Solution::my_atoi("  +0 123".to_string()), 0);
    assert_eq!(Solution::my_atoi("+-12".to_string()), 0);
    assert_eq!(Solution::my_atoi("-+12".to_string()), 0);
    assert_eq!(Solution::my_atoi("+1".to_string()), 1);
    assert_eq!(Solution::my_atoi("+1-1".to_string()), 1);
    assert_eq!(Solution::my_atoi("+199-1-1213daeda".to_string()), 199);
    assert_eq!(Solution::my_atoi("-199+1-1213daeda".to_string()), -199);
    assert_eq!(Solution::my_atoi("42".to_string()), 42);
    assert_eq!(Solution::my_atoi("-042".to_string()), -42);
    assert_eq!(Solution::my_atoi("1337c0d3".to_string()), 1337);
    assert_eq!(Solution::my_atoi("words and 987".to_string()), 0);
    assert_eq!(Solution::my_atoi("0-1".to_string()), 0);
    assert_eq!(Solution::my_atoi("19-abcd-1231".to_string()), 19);
    assert_eq!(Solution::my_atoi("-319-abcd-1231".to_string()), -319);
    assert_eq!(
        Solution::my_atoi("9223372036854775808".to_string()),
        2147483647
    );
    assert_eq!(
        Solution::my_atoi("10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000522545459".to_string()),
        2147483647
    );
}
