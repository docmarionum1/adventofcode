use std::cmp;
use std::error::Error;

fn f(x: i32, y: i32, t: i32) -> (i32, i32) {
    match t {
        0 => (0, 0),
        _ => {
            let mut prev = f(x, y, t - 1);
            prev.0 += cmp::max(0, x - t + 1);
            prev.1 += y - t + 1;

            prev
        }
    }
}

struct BoundingBox {
    x_min: i32,
    x_max: i32,
    y_min: i32,
    y_max: i32,
}

impl BoundingBox {
    fn valid_start(&self, x: i32, y: i32) -> bool {
        let mut i = 0;
        loop {
            let point = f(x, y, i);

            if point.0 > self.x_max || point.1 < self.y_min {
                return false;
            }

            if point.0 >= self.x_min
                && point.0 <= self.x_max
                && point.1 >= self.y_min
                && point.1 <= self.y_max
            {
                return true;
            }

            i += 1;
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let target = BoundingBox {
        x_min: 244,
        x_max: 303,
        y_min: -91,
        y_max: -54,
    };

    // We know that the max height happens when you set your initial y velocity to
    // the abs(min(y)) of the area
    let y_abs = target.y_min.abs() - 1;
    println!(
        "Part 1: {}",
        (0..y_abs * 2).map(|i| f(0, y_abs, i).1).max().unwrap()
    );

    let mut count = 0;

    for x in 0..target.x_max + 1 {
        for y in target.y_min..y_abs + 1 {
            if target.valid_start(x, y) {
                count += 1;
            }
        }
    }

    println!("Part 2: {}", count);

    Ok(())
}
