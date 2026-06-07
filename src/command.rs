use crate::game::Game;

/// Recognized player commands.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Command {
    Go,
    Help,
    Quit,
}

impl Command {
    pub fn from_word(word: &str) -> Option<Self> {
        match word {
            "go" => Some(Self::Go),
            "help" => Some(Self::Help),
            "quit" => Some(Self::Quit),
            _ => None,
        }
    }

    pub fn all_words() -> &'static [&'static str] {
        &["go", "help", "quit"]
    }

    /// Execute the command. Returns `true` when the game should end.
    pub fn execute(&self, game: &mut Game, second_word: Option<&str>) -> bool {
        match self {
            Self::Go => {
                let Some(direction) = second_word else {
                    println!("Go where?");
                    return false;
                };

                let current = game.current_room();
                let Some(next) = game.rooms()[current].exit(direction) else {
                    println!("There is no door!");
                    return false;
                };

                game.set_current_room(next);
                println!("{}", game.rooms()[next].long_description(game.rooms()));
                false
            }
            Self::Help => {
                println!("You are lost. You are alone. You wander");
                println!("around at the university.");
                println!();
                println!("Your command words are:");
                for word in Self::all_words() {
                    print!("{word}  ");
                }
                println!();
                false
            }
            Self::Quit => {
                if second_word.is_some() {
                    println!("Quit what?");
                    false
                } else {
                    true
                }
            }
        }
    }
}
