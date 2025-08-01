pub struct Solution;

impl Solution {
    pub fn convert(s: String, num_rows: i32) -> String {
        let s = s.as_bytes();
        let mut rows: Vec<Vec<u8>> = (0..num_rows).map(|_| vec![]).collect();
        let n: usize = num_rows as usize;

        let mut forward = true;
        let mut idx = 0;
        for c in s {
            // println!("idx={idx} c={c}");
            rows[idx].push(*c);
            if forward {
                if idx == (n - 1) {
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
        rows.into_iter()
            .map(|x| String::from_utf8(x).unwrap())
            .collect::<Vec<_>>()
            .join("")
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
