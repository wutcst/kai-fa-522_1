use std::collections::HashMap;

/// A room in the game world with a description and exits to neighboring rooms.
pub struct Room {
    description: String,
    exits: HashMap<String, usize>,
}

impl Room {
    pub fn new(description: &str) -> Self {
        Self {
            description: description.to_string(),
            exits: HashMap::new(),
        }
    }

    pub fn set_exit(&mut self, direction: &str, neighbor: usize) {
        self.exits.insert(direction.to_string(), neighbor);
    }

    pub fn long_description(&self, rooms: &[Room]) -> String {
        format!("You are {}.\n{}", self.description, self.exit_string(rooms))
    }

    fn exit_string(&self, _rooms: &[Room]) -> String {
        let mut exits: Vec<&str> = self.exits.keys().map(String::as_str).collect();
        exits.sort_unstable();

        let exit_list = exits.join(" ");
        format!("Exits: {exit_list}")
    }

    pub fn exit(&self, direction: &str) -> Option<usize> {
        self.exits.get(direction).copied()
    }
}
