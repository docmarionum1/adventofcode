use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

struct Dot(usize, usize);

#[derive(Debug)]
enum Fold {
    X(usize),
    Y(usize),
}

fn print(paper: &Vec<Vec<bool>>) {
    let output = paper
        .iter()
        .map(|row| {
            row.iter()
                .map(|p| match p {
                    true => "#",
                    false => " ",
                })
                .collect::<Vec<&str>>()
                .join("")
        })
        .collect::<Vec<String>>()
        .join("\n");

    println!("{}", output);
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let mut dots: Vec<Dot> = Vec::new();
    let mut folds: Vec<Fold> = Vec::new();

    for line in reader.lines() {
        let line = line?;

        match line.trim().len() {
            len if len > 9 => {
                // Fold
                let mut split = line.trim()[11..].split("=");
                let axis = split.next().unwrap();
                let coord = split.next().unwrap().parse::<usize>().unwrap();
                if axis == "x" {
                    folds.push(Fold::X(coord));
                } else {
                    folds.push(Fold::Y(coord));
                }
            }
            len if len > 0 => {
                // Dot
                let coords: Vec<usize> = line
                    .trim()
                    .split(",")
                    .map(|c| c.parse::<usize>().unwrap())
                    .collect();
                dots.push(Dot(coords[0], coords[1]));
            }
            _ => {}
        }
    }

    let x_max = dots.iter().map(|dot| dot.0).max().unwrap();
    let y_max = dots.iter().map(|dot| dot.1).max().unwrap();

    let mut paper = vec![vec![false; x_max + 1]; y_max + 1];

    for dot in dots {
        paper[dot.1][dot.0] = true;
    }

    for (i, fold) in folds.iter().enumerate() {
        match fold {
            Fold::X(coord) => {
                let left: Vec<&[bool]> = paper.iter().map(|row| &row[0..*coord]).collect();
                let right: Vec<Vec<&bool>> = paper
                    .iter()
                    .map(|row| row[*coord..].iter().rev().collect::<Vec<&bool>>())
                    .collect();

                paper = left
                    .iter()
                    .zip(right)
                    .map(|(l, r)| l.iter().zip(r).map(|(a, b)| a | *b).collect())
                    .collect();
            }
            Fold::Y(coord) => {
                let top = &paper[0..*coord];
                let bottom = &paper[*coord..];

                paper = top
                    .iter()
                    .zip(bottom.iter().rev())
                    .map(|(l, r)| l.iter().zip(r).map(|(a, b)| a | b).collect())
                    .collect();
            }
        }

        if i == 0 {
            let sum: u32 = paper
                .iter()
                .map(|row| row.iter().map(|v| *v as u32).sum::<u32>())
                .sum();

            println!("Part 1: {}", sum);
        }
    }

    print(&paper);

    Ok(())
}
