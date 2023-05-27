use std::thread;

fn main() {
    let (s1, r) = crossbeam_channel::bounded(10);
    let s2 = s1.clone();
    let r2 = r.clone();

    thread::spawn(move || {
        s1.send(1).unwrap();
        s1.send(3).unwrap();
        s1.send(5).unwrap();
    });
    thread::spawn(move || {
        s2.send(2).unwrap();
        s2.send(4).unwrap();
        s2.send(6).unwrap();
    });

    for _i in 0..3 {
        let msg1 = r.recv().unwrap();
        let msg2 = r.recv().unwrap();
        println!("1 {msg1}");
        println!("1 {msg2}");
    }

    let (s1, r) = crossbeam_channel::bounded(10);
    let s2 = s1.clone();
    let r2 = r.clone();

    thread::spawn(move || {
        s1.send(1).unwrap();
        s1.send(3).unwrap();
        s1.send(5).unwrap();
    });
    thread::spawn(move || {
        s2.send(2).unwrap();
        s2.send(4).unwrap();
        s2.send(6).unwrap();
    });
    for _i in 0..3 {
        let msg1 = r.recv().unwrap();
        let msg2 = r2.recv().unwrap();
        println!("2 {msg1}");
        println!("2 {msg2}");
    }
}
