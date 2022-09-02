use polars::prelude::DataFrame;

/// Split data into train and test
pub fn train_test_split(data: DataFrame, ratio: f32) -> (DataFrame, DataFrame) {
    let train_n = data.height() as f32 * ratio;

    // clean up nulls, no point having them, good data is the priority
    let data = data.agg_chunks().drop_nulls(None).unwrap();

    let data = data.sample_n(data.height(), false, true, None).unwrap();

    let train = data.slice_par(0, train_n as usize);
    let test = data.slice_par(train_n as i64, data.height());
    
    (train, test)
}

/// Label the prediction feature from the rest
pub fn label_predictor(feature: &str, data: DataFrame) {}

// Go through the data analysis pipeline, show user graphs of the data

// Start applying some models to it. And let the user choose what parameters if they really want to
