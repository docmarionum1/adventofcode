use phf::phf_map;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

static POINTS: phf::Map<char, u64> = phf_map! {
    ')' => 3,
    ']' => 57,
    '}' => 1197,
    '>' => 25137,
};

static OPENING: &str = "([{<";
static CLOSING: &str = ")]}>";

enum ParseResult {
    Corrupt(u64),
    Incomplete(u64),
}

fn parse(line: &str) -> ParseResult {
    let mut stack: Vec<char> = Vec::new();

    for c in line.chars() {
        if OPENING.contains(c) {
            stack.push(c);
        } else {
            let matching = stack.pop().unwrap();

            if OPENING.find(matching).unwrap() != CLOSING.find(c).unwrap() {
                return ParseResult::Corrupt(*POINTS.get(&c).unwrap());
            }
        }
    }

    let mut score = 0;
    while !stack.is_empty() {
        let c = stack.pop().unwrap();
        score = score * 5 + OPENING.find(c).unwrap() + 1;
    }

    ParseResult::Incomplete(score.try_into().unwrap())
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let mut corrupt_score: u64 = 0;
    let mut incomplete_scores: Vec<u64> = Vec::new();

    for line in reader.lines() {
        match parse(line?.trim()) {
            ParseResult::Corrupt(n) => corrupt_score += n,
            ParseResult::Incomplete(n) => incomplete_scores.push(n),
        }
    }

    println!("Part 1: {}", corrupt_score);

    incomplete_scores.sort();
    println!("Part 2: {}", incomplete_scores[incomplete_scores.len() / 2]);

    Ok(())
}
