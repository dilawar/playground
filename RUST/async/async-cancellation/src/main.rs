use std::sync::{Arc, Mutex};
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let cancellation_token = CancellationToken::new();
    let token = cancellation_token.clone();

    let task = tokio::spawn(async move {
        tokio::time::sleep(tokio::time::Duration::from_millis(150)).await;
        token.cancel();
    });

    let a = Arc::new(Mutex::new(0));

    tokio::select! {
        _ = task => {
            println!("cancellation token is set.");
        }
        _ = long_task(a.clone()) => {
        }
    };
    println!("a ={}", a.lock().unwrap());
}

async fn long_task(state: Arc<Mutex<i32>>) {
    println!("long task started...");
    {
        let mut lock = state.lock().unwrap();
        *lock += 1;
    }
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    {
        let mut lock = state.lock().unwrap();
        *lock += 1;
    }
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;

    {
        // clean up (reset to 0)
        let mut lock = state.lock().unwrap();
        *lock = 0;
    }
    println!("long_task has ended.");
}
