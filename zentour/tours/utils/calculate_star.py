def calculate_star_ranges(rating):
    rating = rating or 0
    full_stars = int(rating)
    has_half_star = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - int(has_half_star)

    return {
        "full_stars": range(full_stars),
        "has_half_star": has_half_star,
        "empty_stars": range(empty_stars),
    }
