use std::path::Path;
use fts::walkdir::{WalkDir, WalkDirConf};

fn main() {
    let path = Path::new("C:/Program Files");
    for p in WalkDir::new(WalkDirConf::new(path)) {
        println!("{:?}", p.unwrap());
    }
}
