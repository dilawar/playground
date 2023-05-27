use std::thread;

fn main() {
    let (s1, r) = crossbeam_channel::bounded(10);
    let s2 = s1.clone();

    thread::spawn(move || s1.send(1).unwrap());
    thread::spawn(move || s2.send(2).unwrap());

    let msg1 = r.recv().unwrap();
    let msg2 = r.recv().unwrap();

    assert_eq!(msg1 + msg2, 3);
}
