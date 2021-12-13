use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn visited_twice(visted: &HashMap<&str, u8>) -> bool {
    for (k, v) in visted.iter() {
        if *k == k.to_ascii_lowercase() && *v > 1 {
            return true;
        }
    }

    false
}

fn search<'a>(
    caves: &'a HashMap<String, HashSet<String>>,
    node: &'a str,
    visited: &mut HashMap<&'a str, u8>,
    part2: bool,
) -> Vec<Vec<&'a str>> {
    *visited.entry(node).or_default() += 1;

    let mut paths: Vec<Vec<&str>> = Vec::new();

    if node == "end" {
        paths.push(vec!["end"]);
        return paths;
    }

    for connection in caves.get(node).unwrap() {
        if connection == "start" {
            continue;
        }

        if !visited.contains_key(connection.as_str())
            || *connection == connection.to_ascii_uppercase()
            || (part2 && !visited_twice(&visited))
        {
            let results = search(caves, connection, &mut visited.clone(), part2);
            paths.extend(
                results
                    .iter()
                    .map(|path| [vec![node], path.clone()].concat())
                    .collect::<Vec<Vec<&str>>>(),
            );
        }
    }

    paths
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let mut caves: HashMap<String, HashSet<String>> = HashMap::new();

    for line in reader.lines() {
        let line = line?;
        let (a, b) = line.trim().split_once("-").unwrap();
        for (x, y) in [(a, b), (b, a)] {
            caves
                .entry(x.to_string())
                .or_default()
                .insert(y.to_string());
        }
    }

    let mut visited: HashMap<&str, u8> = HashMap::new();
    let paths = search(&caves, "start", &mut visited, false);
    println!("Part 1: {}", paths.len());

    let mut visited: HashMap<&str, u8> = HashMap::new();
    let paths = search(&caves, "start", &mut visited, true);
    println!("Part 2: {}", paths.len());

    Ok(())
}
