use std::path::Path;
use std::time::Instant;
use walkdir::WalkDir;

/// Compute a simple hash of a directory and its children.
fn compute_hash_simple_xor(path: &Path) -> anyhow::Result<u64> {
    let mut total = 0usize;
    let mut hash = 0u64;
    for p in WalkDir::new(path) {
        if p.is_err() {
            continue;
        }
        total += 1;
        if let Ok(metadata) = p.unwrap().metadata() {
            if let Ok(mtime) = metadata.modified() {
                if let Ok(mtime_since) = mtime.duration_since(std::time::SystemTime::UNIX_EPOCH) {
                    hash ^= mtime_since.as_secs();
                }
            }
        }
    }
    hash ^= total as u64;
    Ok(hash)
}

fn main() {
    let path = Path::new("C:/Program Files");

    let now = Instant::now();
    let hash = compute_hash_simple_xor(path);
    let dt = now.elapsed().as_millis();

    println!("Hash of `{}` is {hash:?}. Took {dt} ms", path.display());
}
