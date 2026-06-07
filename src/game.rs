use crate::parser::Parser;
use crate::room::Room;

/// Main game state and loop for World of Zuul.
pub struct Game {
    rooms: Vec<Room>,
    current_room: usize,
    parser: Parser,
}

impl Game {
    pub fn new() -> Self {
        let (rooms, start) = Self::create_rooms();
        Self {
            rooms,
            current_room: start,
            parser: Parser::new(),
        }
    }

    fn create_rooms() -> (Vec<Room>, usize) {
        const OUTSIDE: usize = 0;
        const THEATER: usize = 1;
        const PUB: usize = 2;
        const LAB: usize = 3;
        const OFFICE: usize = 4;

        let mut rooms = vec![
            Room::new("outside the main entrance of the university"),
            Room::new("in a lecture theater"),
            Room::new("in the campus pub"),
            Room::new("in a computing lab"),
            Room::new("in the computing admin office"),
        ];

        rooms[OUTSIDE].set_exit("east", THEATER);
        rooms[OUTSIDE].set_exit("south", LAB);
        rooms[OUTSIDE].set_exit("west", PUB);

        rooms[THEATER].set_exit("west", OUTSIDE);

        rooms[PUB].set_exit("east", OUTSIDE);

        rooms[LAB].set_exit("north", OUTSIDE);
        rooms[LAB].set_exit("east", OFFICE);

        rooms[OFFICE].set_exit("west", LAB);

        (rooms, OUTSIDE)
    }

    pub fn play(&mut self) {
        self.print_welcome();

        let mut finished = false;
        while !finished {
            match self.parser.read_command() {
                None => println!("I don't understand..."),
                Some((command, second_word)) => {
                    finished = command.execute(self, second_word.as_deref());
                }
            }
        }

        println!("Thank you for playing.  Good bye.");
    }

    fn print_welcome(&self) {
        println!();
        println!("Welcome to the World of Zuul!");
        println!("World of Zuul is a new, incredibly boring adventure game.");
        println!("Type 'help' if you need help.");
        println!();
        println!(
            "{}",
            self.rooms[self.current_room].long_description(&self.rooms)
        );
    }

    pub fn current_room(&self) -> usize {
        self.current_room
    }

    pub fn set_current_room(&mut self, room: usize) {
        self.current_room = room;
    }

    pub fn rooms(&self) -> &[Room] {
        &self.rooms
    }
}
