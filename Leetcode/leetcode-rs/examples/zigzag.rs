pub struct Solution;

impl Solution {
    pub fn convert(mut s: String, num_rows: i32) -> String {
        let mut rows: Vec<String> = (0..num_rows).map(|_| "".to_string()).collect();
        let N: usize = num_rows as usize;

        let mut forward = true;
        let mut idx = 0;
        for c in s.drain(..) {
            // println!("idx={idx} c={c}");
            rows[idx].push(c);
            if forward {
                if idx == (N - 1) {
                    forward = false;
                    idx -= 1;
                } else {
                    idx += 1;
                }
            } else if idx == 0 {
                forward = true;
                idx = 1;
            } else {
                idx -= 1;
            }
        }
        // println!("0.0 {s}");
        // println!("0.1 {rows:?}");
        rows.join("")
    }
}

fn main() {
    assert_eq!(
        Solution::convert("PAYPALISHIRING".into(), 3),
        "PAHNAPLSIIGYIR".to_string(),
    );
    assert_eq!(
        Solution::convert("PAYPALISHIRING".into(), 4),
        "PINALSIGYAHRPI".to_string(),
    );
}
