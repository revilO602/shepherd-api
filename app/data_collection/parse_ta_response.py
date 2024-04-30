def parse_response_into_poi(response, poi):
    # Extract basic information
    # poi.location_id = response.get("location_id")
    poi.name = response.get("name")
    poi.description = response.get("description")
    poi.latitude = response.get("latitude")
    poi.longitude = response.get("longitude")

    # Extract rating data
    rating_data = response.get("rating")
    if rating_data is not None:
        poi.rating = float(rating_data)

    ranking_data = response.get("ranking_data", {})
    poi.ranking = ranking_data.get("ranking")
    poi.ranking_out_of = ranking_data.get("ranking_out_of")
    poi.num_reviews = response.get("num_reviews")

    # Initialize an empty list to collect all 'name' values
    name_values = []
    # Extract 'name' value from 'category' object
    if "category" in response and "name" in response["category"]:
        name_values.append(response["category"]["name"])

    # Extract 'name' values from 'subcategory' list
    if "subcategory" in response:
        for subcategory in response["subcategory"]:
            if "name" in subcategory:
                name_values.append(subcategory["name"])

    # Extract 'name' values from 'groups' list
    if "groups" in response:
        for group in response["groups"]:
            if "name" in group:
                name_values.append(group["name"])

    # Extract 'name' values from 'trip_types' list
    if "trip_types" in response:
        for trip_type in response["trip_types"]:
            if "name" in trip_type:
                name_values.append(trip_type["name"])

    # Join all extracted 'name' values into a comma-separated string
    poi.tags = name_values

    return poi
