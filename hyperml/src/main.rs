use log::{debug, LevelFilter};
use polars::prelude::*;
use polars_io::prelude::*;
use simple_logger::SimpleLogger;
use std::{
    env::{self, Args},
    fs::File,
    process::exit,
};

fn main() {
    SimpleLogger::new()
        .with_level(LevelFilter::Debug)
        .without_timestamps()
        .env()
        .init()
        .unwrap();

    let args: Vec<_> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: hyperml <path-to-file.csv>");
        exit(1)
    }
    let path = &args[1];

    // try to open and process the csv
    let data = CsvReader::from_path(path)
        .expect("Couldn't open file, does it exist?")
        .has_header(true)
        .finish()
        .expect("Couldn't process file, is it in the right format?");
    
    input_data(data);
}

fn input_data(data: DataFrame) {
    // debug
    debug!("data = {data}");

    // ask user to specify train or test feature, better to just use clap --predict-feature <feature_name>
}
