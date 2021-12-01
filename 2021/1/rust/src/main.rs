use std::fs::File;
use std::io::{prelude::*, BufReader};

fn main() {
    let file = File::open("../input.txt").expect("Couldn't open");
    //part1(BufReader::new(file));
    part2(BufReader::new(file));
}

fn part1(reader: BufReader<File>) {
    let mut previous = 99999;
    let mut count = 0;

    for line in reader.lines() {
        let current = line.expect("couldn't read line").trim().parse::<u32>().expect("Couldn't parse");
        if current > previous {
            count += 1;
        }
        previous = current;
    }

    println!("{}", count);
}

fn part2(reader: BufReader<File>) {
    let mut count = 0;
    let mut i = 0;
    let (mut window1, mut window2, mut window3, mut window4) = (0, 0, 0, 0);
    let mut lines = reader.lines();

    loop {
        let mut current = 0;
        let mut break_after = false;

        match lines.next() {
            Some(line) => {
                current = line.expect("couldn't read line").trim().parse::<u32>().expect("Couldn't parse");
            },
            None => {
                break_after = true;
            }
        }

        match i % 4 {
            0 => {
                if i >= 4 {
                    if window2 > window1 {
                        count += 1;
                    }
                }
                window1 = current;
                window3 += current;
                window4 += current;
            },
            1 => {
                if i >= 4 {
                    if window3 > window2 {
                        count += 1;
                    }
                }
                window1 += current;
                window2 = current;
                window4 += current;
            },
            2 => {
                if i >= 4 {
                    if window4 > window3 {
                        count += 1;
                    }
                }
                window1 += current;
                window2 += current;
                window3 = current;
            },
            3 => {
                if i >= 4 {
                    if window1 > window4 {
                        count += 1;
                    }
                }
                window2 += current;
                window3 += current;
                window4 = current;
            },
            _ => {}
        }

        if break_after {
            break;
        }

        i += 1;
    }

    println!("{}", count);
}
