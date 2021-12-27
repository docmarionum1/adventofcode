use std::cmp;
use std::cmp::Ordering;
use std::collections::BinaryHeap;
use std::error::Error;
use std::fs::read_to_string;

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    coords: (usize, usize),
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

const NEIGHBORS: [(i32, i32); 4] = [(1, 0), (-1, 0), (0, 1), (0, -1)];

fn shortest_path(map: &Vec<Vec<usize>>) -> usize {
    let mut dist: Vec<Vec<_>> = (0..map.len())
        .map(|_| (0..map[0].len()).map(|_| usize::MAX).collect())
        .collect();
    dist[0][0] = 0;

    let mut heap = BinaryHeap::new();
    heap.push(State {
        cost: 0,
        coords: (0, 0),
    });

    while let Some(State { cost, coords }) = heap.pop() {
        if coords == (map[0].len() - 1, map.len() - 1) {
            return cost;
        }

        if cost > dist[coords.0][coords.1] {
            continue;
        }

        let _: Vec<_> = NEIGHBORS
            .iter()
            .map(|(dx, dy)| {
                map.get((coords.0 as i32 + dy) as usize)
                    .and_then(|row| row.get((coords.1 as i32 + dx) as usize))
                    .map(|c| {
                        let next = State {
                            cost: cost + c,
                            coords: (
                                (coords.0 as i32 + dy) as usize,
                                (coords.1 as i32 + dx) as usize,
                            ),
                        };
                        if next.cost < dist[next.coords.0][next.coords.1] {
                            heap.push(next);
                            dist[next.coords.0][next.coords.1] = next.cost;
                        }
                    })
            })
            .collect();
    }

    0
}

fn main() -> Result<(), Box<dyn Error>> {
    let file = read_to_string("../input.txt").unwrap();

    let map: Vec<Vec<usize>> = file
        .lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).unwrap() as usize)
                .collect()
        })
        .collect();

    println!("Part 1: {}", shortest_path(&map));

    // Construct the larger map
    let mut new_map = map.clone();

    for i in 1..5 {
        for j in 0..map.len() {
            let offset = 100 * (i - 1);
            let slice = &new_map[j][offset..(offset + 100)];
            let slice: Vec<_> = slice.iter().map(|n| cmp::max(1, (n + 1) % 10)).collect();
            new_map[j].extend(slice);
        }
    }

    for i in 1..5 {
        for j in 0..map.len() {
            new_map.push(
                new_map[j + 100 * (i - 1)]
                    .iter()
                    .map(|n| cmp::max(1, (n + 1) % 10))
                    .collect(),
            );
        }
    }

    println!("Part 2: {}", shortest_path(&new_map));

    Ok(())
}
