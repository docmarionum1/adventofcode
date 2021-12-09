use std::cmp::Reverse;
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn is_minima(a: &Vec<Vec<i32>>, i: usize, j: usize) -> bool {
    let n = a[i][j];

    if i > 0 && a[i - 1][j] <= n {
        return false;
    }
    if j > 0 && a[i][j - 1] <= n {
        return false;
    }
    if i < (a.len() - 1) && a[i + 1][j] <= n {
        return false;
    }
    if j < (a.len() - 1) && a[i][j + 1] <= n {
        return false;
    }

    true
}

fn size_of_region(a: &mut Vec<Vec<i32>>, i: usize, j: usize) -> i32 {
    match a[i][j] {
        -1 | 9 => 0,
        _ => {
            let mut s = 1;
            a[i][j] = -1;

            if i > 0 {
                s += size_of_region(a, i - 1, j);
            }
            if j > 0 {
                s += size_of_region(a, i, j - 1);
            }
            if i < (a.len() - 1) {
                s += size_of_region(a, i + 1, j);
            }
            if j < (a.len() - 1) {
                s += size_of_region(a, i, j + 1);
            }

            s
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let mut a: Vec<Vec<i32>> = reader
        .lines()
        .map(|line| {
            line.unwrap()
                .trim()
                .chars()
                .map(|c| i32::try_from(c.to_digit(10).unwrap()).unwrap())
                .collect()
        })
        .collect();

    let mut risk_level: i32 = 0;
    for i in 0..a.len() {
        for j in 0..a.len() {
            if is_minima(&a, i, j) {
                risk_level += 1 + a[i][j];
            }
        }
    }

    println!("Part 1: {}", risk_level);

    let mut sizes: Vec<i32> = Vec::new();

    for i in 0..a.len() {
        for j in 0..a.len() {
            let s = size_of_region(&mut a, i, j);
            if s > 0 {
                sizes.push(s);
            }
        }
    }

    sizes.sort_by_key(|s| Reverse(*s));

    println!("Part 2: {}", sizes[0] * sizes[1] * sizes[2]);

    Ok(())
}
