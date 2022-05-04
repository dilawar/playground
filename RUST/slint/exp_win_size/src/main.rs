use slint;

slint::slint!{
    HelloWorld := Window {
        width: 100px;
        height: 100px;
        Text {
            text: "hello world";
            color: green;
        }
    }
}

fn main() {
    let win = HelloWorld::new();
    println!("width of window is {}", win.get_width());
    win.run();
}
