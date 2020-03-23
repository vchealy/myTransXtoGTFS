attributions.txt
File: Optional

Field Name	Type	Required	Description
attribution_id	ID	Optional	Identifies an attribution for the dataset, or a subset of it. This field is useful for translations.
agency_id	ID referencing	Optional	The agency to which the attribution applies. If one agency_id, route_id, or trip_id attribution is defined, the other fields must be empty. If none are specified, the attribution applies to the whole dataset.
route_id	ID referencing	Optional	This field functions in the same way as agency_id, except the attribution applies to a route. Multiple attributions can apply to the same route.
trip_id	ID referencing	Optional	This field functions in the same way as agency_id, except the attribution applies to a trip. Multiple attributions can apply to the same trip.
organization_name	Text	Required	The name of the organization that the dataset is attributed to.
is_producer	Enum	Optional	The role of the organization is producer. Allowed values include the following:
• 0 or empty: Organization doesn’t have this role.
• 1: Organization does have this role.
At least one of the fields, either is_producer, is_operator, or is_authority, must be set at 1.
is_operator	Enum	Optional	Functions in the same way as is_producer, except the role of the organization is operator.
is_authority	Enum	Optional	Functions in the same way as is_producer, except the role of the organization is authority.
attribution_url	URL	Optional	The URL of the organization.
attribution_email	Email	Optional	The email of the organization.
attribution_phone	Phone number	Optional	The phone number of the organization.