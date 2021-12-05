use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Clone, Copy, Debug)]
struct Point(usize, usize);

#[derive(Debug)]
struct Line(Point, Point);

impl Line {
    fn from(string: String) -> Line {
        let points: Vec<Point> = string
            .split("->")
            .map(|part| {
                let part = part.trim();
                let numbers: Vec<usize> = part
                    .split(",")
                    .map(|num| num.parse::<usize>().unwrap())
                    .collect();
                Point(numbers[0], numbers[1])
            })
            .collect();
        Line(points[0], points[1])
    }

    fn is_horizontal(&self) -> bool {
        self.0 .1 == self.1 .1
    }
    fn is_vertical(&self) -> bool {
        self.0 .0 == self.1 .0
    }

    fn is_diagonal(&self) -> bool {
        !self.is_vertical() && !self.is_horizontal()
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let reader = BufReader::new(file);

    let mut grid: [[u32; 999]; 999] = [[0; 999]; 999];

    let part2 = true;

    for line in reader.lines() {
        let line = Line::from(line?);

        if part2 && line.is_diagonal() {
            let x_rev = line.0 .0 > line.1 .0;
            let y_rev = line.0 .1 > line.1 .1;
            let xs: Vec<usize> = match x_rev {
                false => (line.0 .0..=line.1 .0).collect(),
                true => (line.1 .0..=line.0 .0).rev().collect(),
            };
            let ys: Vec<usize> = match y_rev {
                false => (line.0 .1..=line.1 .1).collect(),
                true => (line.1 .1..=line.0 .1).rev().collect(),
            };
            let points = xs.iter().zip(ys);

            for (i, j) in points {
                grid[*i][j] += 1;
            }
        } else if line.is_horizontal() {
            let j = line.0 .1;
            let mut xs = [line.0 .0, line.1 .0];
            xs.sort();
            for i in xs[0]..=xs[1] {
                grid[i][j] += 1;
            }
        } else if line.is_vertical() {
            let i = line.0 .0;
            let mut ys = [line.0 .1, line.1 .1];
            ys.sort();
            for j in ys[0]..=ys[1] {
                grid[i][j] += 1;
            }
        }
    }

    let mut count = 0;

    for i in 0..999 {
        for j in 0..999 {
            if grid[i][j] > 1 {
                count += 1;
            }
        }
    }

    println!("{}", count);

    Ok(())
}
