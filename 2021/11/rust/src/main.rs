use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn flash(a: &mut Vec<Vec<i32>>, num_flashes: &mut i32, i: i32, j: i32) {
    *num_flashes += 1;

    for x in -1..=1 {
        for y in -1..=1 {
            if x == 0 && y == 0 {
                continue;
            }

            match a.get_mut((i + x) as usize) {
                Some(b) => match b.get_mut((j + y) as usize) {
                    Some(v) => {
                        *v += 1;

                        if *v == 10 {
                            flash(a, num_flashes, i + x, j + y);
                        }
                    }
                    None => {}
                },
                None => {}
            }
        }
    }
}

fn run_step(a: &mut Vec<Vec<i32>>, num_flashes: &mut i32) -> bool {
    for i in 0..a.len() {
        for j in 0..a.len() {
            a[i][j] += 1;
            if a[i][j] == 10 {
                flash(a, num_flashes, i as i32, j as i32);
            }
        }
    }

    let mut all_flash = true;

    for i in 0..a.len() {
        for j in 0..a.len() {
            if a[i][j] > 9 {
                a[i][j] = 0;
            } else {
                all_flash = false;
            }
        }
    }

    all_flash
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

    let mut num_flashes = 0;

    for _ in 0..100 {
        run_step(&mut a, &mut num_flashes);
    }

    println!("Part 1: {}", num_flashes);

    let mut step = 100;

    loop {
        step += 1;
        if run_step(&mut a, &mut num_flashes) {
            println!("Part 2: {}", step);
            break;
        }
    }

    Ok(())
}
