use dioxus::prelude::{dioxus_elements::div, *};

pub fn app(cx: Scope) -> Element {
    let mut count = use_state(&cx, || 0);

    let container_style = r#"
        display: flex;
        flex-direction: column;
        align-items: center;
    "#;

    let rect_style = r#"
        background: deepskyblue;
        height: 50vh;
        width: 50vw;
    "#;

    cx.render(rsx! {
        button { onclick: move |_| count += 1, "Click me to increment!" }
        div {"Hello BUDGET!!!!!"}
        div {
            style: "{container_style}",
        }
    })
}

fn main() {
    dioxus::web::launch(app);
}
