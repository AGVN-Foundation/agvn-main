fn main() {}

// ------------
// TOKENS
// ------------

// tokens of the english language
// words that are defined are tokenised into a one-hot encoded val or just some number
// words undefined should be matched to its closest defined word in terms of spelling
// grammar tokens like ,.? are also taken
pub struct EnglishToken;

// ------------
// TRANSFORMER
// ------------

pub type Size = u128;

pub struct Transformer {
    // cached vals, could prob make them methods instead
    n_encoders: Size,
    n_decoders: Size,
    // the bulk of the model
    encoders: Vec<Encoder>,
    decoders: Vec<Decoder>,
    // extra params like softmax and randomisation parameters
    
}

impl Transformer {
    /// Takes in a stream (list) of tokens
    /// Best to just pass by ref
    /// And train as soon as new data arrives
    pub fn train_ad_hoc(tokens: &[EnglishToken]) {}

    /// Given a stream of tokens, try to complete it as best as possible to some index
    /// If no next word would be a suitable threshold fit, then back out
    /// Also has 'safe mode' that generates more stable sentences based on known seeds
    pub fn complete_sentence(tokens: &[EnglishToken]) {}
}

// ------------
// ENCODER
// ------------

// input goes through multiple encoder units
// sequentially. The last one then feeds n decoders in parallel
pub struct Encoder;

// takes in streams of tokens
pub struct SelfAttentionUnit {}

pub struct FeedForwardUnit {}

// ------------
// DECODER
// ------------

pub struct Decoder;
