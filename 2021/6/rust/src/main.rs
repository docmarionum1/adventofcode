use cached::proc_macro::cached;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[cached]
fn num_children(days: i32) -> u64 {
    let mut num: u64 = 1;
    if days - 7 > 0 {
        num += num_children(days - 7);
    }
    if days - 9 > 0 {
        num += num_children(days - 9);
    }

    num
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let mut reader = BufReader::new(file);

    // Read the inputs
    let mut line = String::new();
    reader.read_line(&mut line)?;
    let mut numbers: Vec<i32> = line
        .trim()
        .split(",")
        .into_iter()
        .map(|number| number.to_string().parse::<i32>().unwrap())
        .collect();

    let num_days = 256;
    let mut num_fish = 0;

    for fish in numbers {
        num_fish += num_children(num_days - fish) + 1;
    }

    println!("{}", num_fish);

    Ok(())
}
