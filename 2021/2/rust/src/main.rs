use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("../input.txt").expect("Couldn't open");
    let reader = BufReader::new(file);

    // Variables for part 1
    let mut h1 = 0;
    let mut d1 = 0;

    // Variables for part 2
    let mut d2 = 0;
    let mut aim = 0;

    for line in reader.lines() {
        //println!("{:?}", line);
        match line {
            Ok(s) => {
                let v: Vec<&str> = s.trim().split(" ").collect();
                let x: u32 = v[1].parse().expect("Couldn't parse number");
                match v[0] {
                    "forward" => {
                        h1 += x;
                        d2 += (aim * x);
                    }
                    "down" => {
                        d1 += x;
                        aim += x;
                    }
                    "up" => {
                        d1 -= x;
                        aim -= x;
                    }
                    _ => {}
                }
            }
            _ => {}
        }
    }

    println!("Part 1: {}", h1 * d1);
    println!("Part 2: {}", h1 * d2);
}
