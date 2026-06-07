mod command;
mod game;
mod parser;
mod room;

use game::Game;

fn main() {
    let mut game = Game::new();
    game.play();
}
