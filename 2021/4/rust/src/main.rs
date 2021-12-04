use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

#[derive(Clone, Debug)]
struct Cell(u32, bool);

struct Board {
    board: Vec<Vec<Cell>>,
    won: bool,
}

fn check_winner(board: &Vec<Vec<Cell>>) -> bool {
    'row_outer: for row in 0..5 {
        for cell in 0..5 {
            if !board[row][cell].1 {
                continue 'row_outer;
            }
        }
        return true;
    }

    'col_outer: for col in 0..5 {
        for cell in 0..5 {
            if !board[cell][col].1 {
                continue 'col_outer;
            }
        }
        return true;
    }

    false
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("../input.txt")?;
    let mut reader = BufReader::new(file);

    // Read the inputs
    let mut line = String::new();
    reader.read_line(&mut line)?;
    let numbers: Vec<u32> = line
        .trim()
        .split(",")
        .into_iter()
        .map(|number| number.to_string().parse::<u32>().unwrap())
        .collect();

    let mut boards: Vec<Board> = Vec::new();
    let mut current_board: Board = Board {
        board: Vec::new(),
        won: false,
    };

    reader.read_line(&mut line)?; // Skip the first new line
    for line in reader.lines() {
        let line = line.unwrap();
        let line = line.trim();
        if line.len() == 0 {
            boards.push(current_board);
            current_board = Board {
                board: Vec::new(),
                won: false,
            };
        } else {
            let row: Vec<Cell> = line
                .split_whitespace()
                .map(|number| Cell(number.to_string().parse::<u32>().unwrap(), false))
                .collect();
            current_board.board.push(row);
        }
    }

    boards.push(current_board);

    let mut num_winners = 0;

    for number in numbers {
        // Update boards
        for i in 0..boards.len() {
            for j in 0..5 {
                for k in 0..5 {
                    if boards[i].board[j][k].0 == number {
                        boards[i].board[j][k].1 = true;
                    }
                }
            }
        }

        for i in 0..boards.len() {
            let board = &mut boards[i]; // Key here was making the right side &mut to borrow as mutable
            if !board.won && check_winner(&board.board) {
                board.won = true;
                num_winners += 1;
                if num_winners == 1 || num_winners == 100 {
                    let mut sum = 0;
                    for row in &board.board {
                        for cell in row {
                            if !cell.1 {
                                sum += cell.0;
                            }
                        }
                    }
                    println!("Winner {}: {}", num_winners, sum * number);
                }
            }
        }
    }

    Ok(())
}
