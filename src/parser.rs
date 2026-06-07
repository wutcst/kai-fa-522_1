use std::io::{self, Write};

use crate::command::Command;

/// Reads and tokenizes player input into commands.
pub struct Parser;

impl Parser {
    pub fn new() -> Self {
        Self
    }

    pub fn read_command(&self) -> Option<(Command, Option<String>)> {
        print!("> ");
        io::stdout().flush().ok()?;

        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).ok()?;

        let mut words = input_line.split_whitespace();
        let word1 = words.next()?;
        let word2 = words.next().map(str::to_string);

        let command = Command::from_word(word1)?;
        Some((command, word2))
    }
}
