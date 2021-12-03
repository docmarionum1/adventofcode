use std::fs::File;
use std::io::{BufRead, BufReader, Seek, SeekFrom};

#[derive(Clone, Debug)]
struct BitCount(u64, u64);

fn main() {
    let file = File::open("../input.txt").expect("Couldn't open");
    let mut reader = BufReader::new(file);

    // Figure out how many bits
    let mut line = String::new();
    let len = match reader.read_line(&mut line) {
        Ok(s) => s - 1,
        _ => panic!("Couldn't read first line"),
    };
    reader.seek(SeekFrom::Start(0));
    println!("{}", len);

    part1(&mut reader, len);

    reader.seek(SeekFrom::Start(0));
    let oxygen = part2(&mut reader, len, true);
    reader.seek(SeekFrom::Start(0));
    let co2 = part2(&mut reader, len, false);
    println!("Part 2: {}", oxygen * co2);
}

fn read_file(reader: &mut BufReader<File>) -> Vec<String> {
    let mut numbers: Vec<String> = Vec::new();

    for line in reader.lines() {
        match line {
            Ok(s) => {
                numbers.push(s.trim().to_string());
            }
            _ => break,
        }
    }

    numbers
}

fn part2(reader: &mut BufReader<File>, len: usize, oxygen: bool) -> u32 {
    let mut numbers = read_file(reader);

    let mut i = 0;

    while numbers.len() > 1 {
        let mut counts = vec![BitCount(0, 0); len];
        counts = get_counts(&numbers, counts);

        let mut target = b'0';

        if oxygen {
            if counts[i].1 >= counts[i].0 {
                target = b'1';
            }
        } else {
            if counts[i].1 < counts[i].0 {
                target = b'1';
            }
        }

        let mut new_numbers: Vec<String> = Vec::new();

        for num in numbers {
            let bytes = num.as_bytes();

            if bytes[i] == target {
                new_numbers.push(num);
            }
        }

        numbers = new_numbers;

        i += 1;
    }

    u32::from_str_radix(&numbers[0], 2).unwrap()
}

fn get_counts(numbers: &Vec<String>, mut counts: Vec<BitCount>) -> Vec<BitCount> {
    for num in numbers {
        let bytes = num.trim().as_bytes();

        for (i, &item) in bytes.iter().enumerate() {
            match item {
                b'0' => counts[i].0 += 1,
                b'1' => counts[i].1 += 1,
                _ => {}
            }
        }
    }

    counts
}

fn part1(reader: &mut BufReader<File>, len: usize) {
    let mut numbers = read_file(reader);
    let mut counts = vec![BitCount(0, 0); len];
    counts = get_counts(&numbers, counts);

    let mut gamma: u64 = 0;
    let mut epsilon: u64 = 0;

    for (i, c) in counts.iter().enumerate() {
        if c.0 > c.1 {
            epsilon += 1 << (len - i - 1);
        } else {
            gamma += 1 << (len - i - 1);
        }
    }

    println!("Part 1: {}", gamma * epsilon);
}
