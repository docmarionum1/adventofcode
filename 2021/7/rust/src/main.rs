use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let mut reader = BufReader::new(file);
    let mut line = String::new();
    reader.read_line(&mut line)?;
    let numbers: Vec<i64> = line
        .trim()
        .split(",")
        .into_iter()
        .map(|n| n.to_string().parse::<i64>().unwrap())
        .collect();

    // Part 1
    let r = (1..999)
        .map(|i| numbers.iter().map(|n| (n - i).abs()).sum::<i64>())
        .into_iter()
        .min();
    println!("Part 1: {}", r.unwrap());

    // Part 2
    let r = (1..999)
        .map(|i| {
            numbers
                .iter()
                .map(|n| {
                    let x = (n - i).abs();
                    x * (x + 1) / 2
                })
                .sum::<i64>()
        })
        .into_iter()
        .min();
    println!("Part 2: {}", r.unwrap());

    Ok(())
}
