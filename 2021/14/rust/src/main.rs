use cached::proc_macro::cached;
use std::collections::HashMap;
use std::error::Error;
use std::fs::read_to_string;

static mut RULES: Option<HashMap<String, String>> = None;

#[cached]
fn expand(pair: String, steps: u8) -> HashMap<String, u64> {
    if steps == 0 {
        return HashMap::new();
    }

    unsafe {
        match &RULES {
            Some(r) => {
                let middle_char = &r[&pair];

                let mut left_pair = pair[0..1].to_string();
                left_pair.push_str(&middle_char);
                let mut result = expand(left_pair, steps - 1);

                let mut right_pair = String::from(middle_char);
                right_pair.push_str(&pair[1..2]);
                let result_right = expand(right_pair, steps - 1);

                for (k, v) in result_right {
                    *result.entry(k).or_default() += v;
                }

                *result.entry(middle_char.to_string()).or_default() += 1;
                result
            }
            None => HashMap::new(),
        }
    }
}

fn get_counts(steps: u8, template: &str) -> u64 {
    let mut counts: HashMap<String, u64> = HashMap::new();
    for i in 0..template.len() {
        let c = &template[i..i + 1];
        *counts.entry(c.to_string()).or_default() += 1;

        if i < (template.len() - 1) {
            let pair = &template[i..i + 2];
            let result = expand(String::from(pair), steps);

            for (k, v) in result {
                *counts.entry(k.to_string()).or_default() += v;
            }
        }
    }

    let min = counts.values().min().unwrap();
    let max = counts.values().max().unwrap();

    max - min
}

fn parse_line(line: &&str) -> (String, String) {
    let tuple = line.split_once(" -> ").unwrap();

    (tuple.0.to_string(), tuple.1.to_string())
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = read_to_string("../input.txt").unwrap();
    let lines = file.lines().collect::<Vec<&str>>();

    let template = lines[0];

    unsafe {
        RULES = Some(lines[2..].iter().map(parse_line).collect());
        println!("Part 1: {}", get_counts(10, template));
        println!("Part 2: {}", get_counts(40, template));
    }

    Ok(())
}
