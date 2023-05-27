fn main() {
    let connection = zbus::blocking::Connection::session().unwrap();
    let manager = geoclue_zbus::ManagerProxyBlocking::new(&connection);
    println!("Done");
}
