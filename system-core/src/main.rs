use linfa::prelude::*;
use linfa_svm::{error::Result, Svm};

fn main() -> Result<()> {
    // BOILERPLATE LINFA

    // classification hueristic: quality > 6.5 is good wine
    let (train, valid) = linfa_datasets::winequality()
        .map_targets(|x| *x > 6)
        .split_with_ratio(0.9);

    println!(
        "Fit SVM classifier with #{} training points",
        train.nsamples()
    );

    // fit an SVM with C value 7 and 0.6 for positive and negative classes
    let model = Svm::<_, bool>::params()
        .pos_neg_weights(50000., 5000.)
        .gaussian_kernel(80.0)
        .fit(&train)?;

    println!("{}", model);
    // A positive prediction indicates a good wine, a negative, a bad one
    fn tag_classes(x: &bool) -> String {
        if *x {
            "good".into()
        } else {
            "bad".into()
        }
    }

    // map targets for validation dataset
    let valid = valid.map_targets(tag_classes);

    // predict and map targets
    let pred = model.predict(&valid).map(tag_classes);

    // create a confusion matrix
    let cm = pred.confusion_matrix(&valid)?;

    println!("{:?}", cm);

    // accuracy of predictions + matthew correlation coeff (phi)
    println!("accuracy {}, MCC {}", cm.accuracy(), cm.mcc());

    Ok(())
}
