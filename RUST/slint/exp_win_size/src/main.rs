use slint;

slint::slint!{
    HelloWorld := Window {
        width: 100px;
        height: 100px;
        // https://github.com/slint-ui/slint/discussions/1229
        property window_width <=> width;
        property window_height <=> height;
        Text {
            text: "hello world";
            color: green;
        }
    }
}

fn main() {
    let win = HelloWorld::new();
    println!("width of window is {}", win.get_window_width());
    win.run();
}
