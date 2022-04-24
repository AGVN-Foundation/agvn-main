fn main() {}

// ------------
// TRANSFORMER
// ------------

struct Transformer;

// ------------
// ENCODER
// ------------

// input goes through multiple encoder units
// sequentially. The last one then feeds n decoders in parallel
struct Encoder;

// takes in streams of tokens
struct SelfAttentionUnit {}

struct FeedForwardUnit {}

// ------------
// DECODER
// ------------

struct Decoder;
