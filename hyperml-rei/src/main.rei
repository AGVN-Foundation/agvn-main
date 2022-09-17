#*
    AutoML Library
*#

// NOTE: overloading main is only supported on std for now

type ReadError = SString
const READ_EXCEPTION = "Couldn't read file!"

fn main(files: String...) -> () | ReadError {
    let data_collection = []

    files.for_each(
        f => {
            let file_contents = read_file(f)?
            let dataframe = parse_contents(file_contents)?
            data_collection.append(dataframe)
        }
    )
}

fn parse_contents(file_contents: String) -> _ {
    parse_csv(file_contents)
}

fn read_file(filepath: String) -> _ {
    read_to_string()? : READ_EXCEPTION
}

/*
statement!

match s {
    Ok(s) => return s
    Err(e) => e
}

statement?

match s {
    Ok(s) => s
    Err(e) => return e
}
*/

// how does expr1 ? : expr2 work?
// if expr1 evals to Ok or true, it will return expr1 
// otherwise it will return expr2

// -> _ type inference isnt really that good, since you may write realyl bad code that doesnt show your intent as well
