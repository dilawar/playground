use dns_lookup::lookup_addr;
use std::net;


fn main() {
    let ip : std::net::IpAddr = "13.251.155.22".parse().unwrap();
    let host = lookup_addr(&ip).unwrap();
    println!("{} -> {}", ip, host);
}
