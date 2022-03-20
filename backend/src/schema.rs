// auto-updated everytime we run/revert a migration (migrate, not makemigrations?)

table! {
    posts (id) {
        id -> Integer,
        title -> Text,
        body -> Text,
        published -> Bool,
    }
}
