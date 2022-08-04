use dioxus::prelude::{dioxus_elements::div, *};

#[derive(Debug, PartialEq, Eq)]
pub enum FlexDir {
    Row,
    Column,
}

#[derive(PartialEq, Props)]
pub struct FlexProps {
    flex: FlexDir,
}

pub fn Flex(cx: Scope<FlexProps>) -> Element {
    cx.render(rsx!(div {
        flex_direction: "column",
        padding: "2",
        "This is a Flex!",
        "This is some more text"
    }))
}
