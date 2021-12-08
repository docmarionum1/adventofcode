use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str;

fn sort_string(s: &str) -> String {
    let mut s: Vec<u8> = Vec::from(s.as_bytes());
    s.sort();
    String::from_utf8(s).unwrap()
}

fn decode(signals: &str) -> HashMap<String, u32> {
    let mut lens: HashMap<usize, Vec<String>> = HashMap::new();
    let signals = signals.trim().split_whitespace();
    for signal in signals {
        let l = lens.entry(signal.len()).or_default();
        l.push(sort_string(signal));
    }

    let mut mapping: HashMap<u32, String> = HashMap::new();
    for k in [0, 2, 3, 5, 6, 9] {
        mapping.insert(k, String::from(""));
    }
    mapping.insert(1, lens.entry(2).or_default()[0].clone());
    mapping.insert(4, lens.entry(4).or_default()[0].clone());
    mapping.insert(7, lens.entry(3).or_default()[0].clone());
    mapping.insert(8, lens.entry(7).or_default()[0].clone());

    for signal in lens.entry(6).or_default() {
        let one_set: HashSet<char> = HashSet::from_iter(mapping.entry(1).or_default().chars());
        let four_set: HashSet<char> = HashSet::from_iter(mapping.entry(4).or_default().chars());
        let signal_set: HashSet<char> = HashSet::from_iter(signal.chars());

        if signal_set.intersection(&one_set).count() == 1 {
            mapping.insert(6, signal.to_string());
        } else if signal_set.intersection(&four_set).count() == 4 {
            mapping.insert(9, signal.to_string());
        } else {
            mapping.insert(0, signal.to_string());
        }
    }

    for signal in lens.entry(5).or_default() {
        let one_set: HashSet<char> = HashSet::from_iter(mapping.entry(1).or_default().chars());
        let nine_set: HashSet<char> = HashSet::from_iter(mapping.entry(9).or_default().chars());
        let signal_set: HashSet<char> = HashSet::from_iter(signal.chars());

        if signal_set.intersection(&one_set).count() == 2 {
            mapping.insert(3, signal.to_string());
        } else if signal_set.intersection(&nine_set).count() == 5 {
            mapping.insert(5, signal.to_string());
        } else {
            mapping.insert(2, signal.to_string());
        }
    }

    mapping.into_iter().map(|(k, v)| (v, k)).collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let ten: u32 = 10;
    let mut count = 0;
    let mut sum = 0;

    for line in reader.lines() {
        let line = line?;
        let split: Vec<&str> = line.trim().split("|").collect();
        let (signals, output) = (split[0], split[1]);

        let mapping = decode(signals);

        for (i, digit) in output.trim().split_whitespace().enumerate() {
            let digit = sort_string(digit);

            // Part 1
            match digit.len() {
                2 | 3 | 4 | 7 => count += 1,
                _ => {}
            }

            // Part 2
            sum += *mapping.get(&digit).unwrap() * ten.pow((3 - i).try_into().unwrap());
        }
    }

    println!("Part 1: {}", count);
    println!("Part 2: {}", sum);

    Ok(())
}
