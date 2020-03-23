File: Optional

Frequencies.txt represents trips that operate on regular headways (time between trips). This file can be used to represent two different types of service.

Frequency-based service (exact_times=0) in which service does not follow a fixed schedule throughout the day. Instead, operators attempt to strictly maintain predetermined headways for trips.
A compressed representation of schedule-based service (exact_times=1) that has the exact same headway for trips over specified time period(s). In schedule-based service operators try to strictly adhere to a schedule.
Field Name	Type	Required	Description
trip_id	ID referencing trips.trip_id	Required	Identifies a trip to which the specified headway of service applies.
start_time	Time	Required	Time at which the first vehicle departs from the first stop of the trip with the specified headway.
end_time	Time	Required	Time at which service changes to a different headway (or ceases) at the first stop in the trip.
headway_secs	Non-negative integer	Required	Time, in seconds, between departures from the same stop (headway) for the trip, during the time interval specified by start_time and end_time. Multiple headways for the same trip are allowed, but may not overlap. New headways may start at the exact time the previous headway ends.
exact_times	Enum	Optional	Indicates the type of service for a trip. See the file description for more information. Valid options are:

0 or empty - Frequency-based trips.
1 - Schedule-based trips with the exact same headway throughout the day. In this case the end_time value must be greater than the last desired trip start_time but less than the last desired trip start_time + headway_secs.