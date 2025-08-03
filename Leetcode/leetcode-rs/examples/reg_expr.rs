pub struct Solution;

impl Solution {
    pub fn is_match(mut s: String, mut p: String) -> bool {
        eprintln!(" Input=`{s}` and pattern p=`{p}`.");
        let mut s = s.into_bytes();
        let mut p = p.into_bytes();

        let mut si = 0;
        let mut pi = 0;

        while si < s.len() && pi < p.len() {
            let x = s[si];
            let y = p[pi];

            eprintln!("> si={si} x={}, pi={pi} y={}", x as char, y as char);

            // check if next char is '*' in the pattern. if yes, we handle this situation differently.
            let y1 = p.get(pi + 1);
            if y1 == Some(&b'*') {
                // consume as many prev as possible.
                eprintln!("Next char is *, curr is {}", x as char);
                if y == b'.' {
                    // any character is fair game.
                    si += 1;
                    pi += 1;
                    continue;
                }

                // consume as many x as possible.
                eprintln!("Consuming zero or more chars. si={si}.");
                while Some(&x) == s.get(si) {
                    si += 1;
                }
                eprintln!(" consumed ={si}.");
                // '*' is processed to jump to next.
                pi += 1;
            } else {
                println!("--> next char is not '*'");
                if x == b'.' {
                    // any char matches.
                    si += 1;
                    pi += 1;
                } else {
                    if s.get(si) != p.get(pi) {
                        return false;
                    }
                    si += 1;
                    pi += 1;
                }
            }
        }

        eprintln!(" all done ");

        true
    }
}

fn main() {
    println!("0.9 ==================");
    assert_eq!(Solution::is_match("abcd".into(), "ab.e".into()), false);
    println!("0.0 ==================");
    assert_eq!(Solution::is_match("aa".into(), "a".into()), false);
    println!("0.1 ==================");
    assert_eq!(Solution::is_match("aa".into(), "a*".into()), true);
    println!("0.2 ==================");
    assert_eq!(Solution::is_match("aa".into(), "aab*".into()), true);
    println!("0.3 ==================");
    assert_eq!(Solution::is_match("aa".into(), "aax*".into()), true);
    println!("0.4 ==================");
    assert_eq!(Solution::is_match("ab".into(), ".*".into()), true);
    println!("0.5 ==================");
    assert_eq!(Solution::is_match("abcd".into(), "ab.*".into()), true);
    println!("0.6 ==================");
    assert_eq!(Solution::is_match("abcd".into(), "ab.*".into()), true);
    println!("0.7 ==================");
    assert_eq!(Solution::is_match("abcd".into(), "ab.d".into()), true);
    println!("0.8 ==================");
    assert_eq!(Solution::is_match("abcd".into(), "ab..".into()), true);
}
