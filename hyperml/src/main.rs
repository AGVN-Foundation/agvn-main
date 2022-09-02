use polars::prelude::*;
use polars_io::prelude::*;
use std::fs::File;

fn main() {
    println!("Hello, world!");

    let data = CsvReader::from_path("examples/datasets/world-population.csv")
        .unwrap()
        .has_header(true)
        .finish()
        .unwrap();

    let head = data.head(Some(5));
    println!("head = {head}");
}

fn input_data(data: DataFrame) {}
