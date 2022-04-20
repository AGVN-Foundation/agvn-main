extern crate backend;
extern crate diesel;

use self::backend::*;

fn main() {
    let connection = establish_connection();

    let title = "Hello, World!";
    let body = "This is some text";

    let post = create_post(&connection, title, &body);
    println!("\nSaved draft {} with id {}", title, post.id);
}
