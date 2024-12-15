mod window_position;

fn main() {
    let pos = window_position::get_window_position("Kindle");
    dbg!(pos);
}
