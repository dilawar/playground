pub struct Solution;

impl Solution {
    pub fn my_atoi(s: String) -> i32 {
        let mut result = 0i64;
        let mut is_neg = false;
        let mut is_pos = false;
        let mut m = 0;

        for c in s.as_bytes().iter().rev() {
            if *c == b' ' {
                continue;
                if result > 0 {
                    break;
                }
            }

            // This should be the last character but it can also occur in between.
            if *c == b'-' {
                is_neg = true;
                if is_pos {
                    m = 0;
                    result = 0;
                }
                continue;
            }
            if *c == b'+' {
                is_pos = true;
                if is_neg {
                    m = 0;
                    result = 0;
                }
                continue;
            }

            let v = *c - b'0';
            if v > 9 {
                eprintln!("{c} is not a digit. Reset!");
                result = 0;
                m = 0;
                is_neg = false;
                continue;
            }

            // valid digit, check if - came before it. If yes, then ignore it.
            if (is_neg || is_pos) {
                eprintln!("-/+ was seen before. Ignoring previous result.");
                m = 0;
                result = 0;
                is_neg = false;
                is_pos = false;
            }

            result += (v as i64 * 10_i64.pow(m));
            result = result.min(i64::MAX);
            eprintln!(" value = {v}, result= {result}.");
            m += 1;
        }

        if is_neg {
            result = -result;
        }

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
}
