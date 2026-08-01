use std::sync::{Arc, Mutex};
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let a = Arc::new(Mutex::new(0));
    let a1 = a.clone();

    let cancellation_token = CancellationToken::new();
    let token = cancellation_token.clone();

    let task = tokio::spawn(async move {
        tokio::time::sleep(tokio::time::Duration::from_millis(150)).await;
        token.cancel();
    });

    tokio::select! {
        _ = task => {
            println!("cancelled");
        }
        _ = long_task(a1) => {
            println!("long task over");
        }
    };
    println!("a ={}", a.lock().unwrap());
}

async fn long_task(state: Arc<Mutex<i32>>) {
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
        let mut lock = state.lock().unwrap();
        *lock += 1;
    }
    tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
}
