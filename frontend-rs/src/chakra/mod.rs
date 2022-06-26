use dioxus::prelude::*;

pub fn example(cx: Scope) -> Element {
    cx.render(rsx!("hello world!"))
}
