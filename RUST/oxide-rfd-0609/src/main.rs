use futures::{FutureExt, future};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::Mutex;
use tokio::time::sleep;

#[tokio::main]
async fn main() {
    // Create a lock that will be shared by multiple tasks.
    let lock = Arc::new(Mutex::new(()));

    // Start a background task that takes the lock and holds it for a few
    // seconds.  This is just to simulate some contention.  This function only
    // returns once the lock has been taken in the background task.
    start_background_task(lock.clone()).await;

    // The guts of the example.
    do_stuff(lock.clone()).await;
}

// Starts a background task that grabs the lock, holds it for 5 seconds,
// and then drops it.  Returns once the task is holding the lock.
// The purpose of this is to simulate contention.
async fn start_background_task(lock: Arc<Mutex<()>>) {
    // Use a channel to coordinate with the task so that it can tell us when
    // its taken the lock.
    let (tx, rx) = tokio::sync::oneshot::channel();
    let _ = tokio::spawn(async move {
        println!("[bg] start");
        let _guard = lock.lock().await;
        println!("[bg] sending oneshot message");
        let _ = tx.send(());
        println!("[bg] sent oneshot message. now sleeping for 5s");
        sleep(Duration::from_secs(5)).await;
        println!("[bg] done (dropping lock)")
    });
    // Wait for the task to take the lock before returning.
    let _ = rx.await;
    println!("[bg] lock acquired.");
}

// The guts of the example
async fn do_stuff(lock: Arc<Mutex<()>>) {
    // let mut future1 = do_async_thing("op1", lock.clone()).boxed();
    let future1 = do_async_thing("op1", lock.clone());
    tokio::pin!(future1);

    // Try to execute `future1`.  If it takes more than 500ms, do
    // a related thing instead.
    println!("do_stuff: entering select");
    tokio::select! {
        _ = &mut future1 => {
            println!("do_stuff: arm1 future finished");
        }
        _ = sleep(Duration::from_millis(500)) => {
            do_async_thing("op2", lock.clone()).await;
        }
    };
    println!("do_stuff: all done");
}

async fn do_async_thing(label: &str, lock: Arc<Mutex<()>>) {
    println!("{label}: started");
    let _ = lock.lock().await;
    println!("{label}: acquired lock");
    println!("{label}: done");
}
