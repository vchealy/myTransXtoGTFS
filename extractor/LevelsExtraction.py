File: Optional

Describe the different levels of a station. Is mostly useful when used in conjunction with pathways.txt, and is required for elevator (pathway_mode=5) to ask the user to take the elevator to the “Mezzanine” or the “Platform” level.

Field Name	Type	Required	Description
level_id	ID	Required	Id of the level that can be referenced from stops.txt.
level_index	Float	Required	Numeric index of the level that indicates relative position of this level in relation to other levels (levels with higher indices are assumed to be located above levels with lower indices).

Ground level should have index 0, with levels above ground indicated by positive indices and levels below ground by negative indices.
level_name	Text	Optional	Optional name of the level (that matches level lettering/numbering used inside the building or the station). Is useful for elevator routing (e.g. “take the elevator to level “Mezzanine” or “Platforms” or “-1”).