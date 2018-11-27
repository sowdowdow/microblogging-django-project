from Microlly.models import Post
def get_rank(number_of_posts):
    try:
        points = int(number_of_posts)
    except:
        points = 0

    ranks = [
        "Luke",
        "Platinium",
        "Gold",
        "Silver",
        "Bronze",
        "Noob",
    ]
    if points >= 10000:
        return ranks[0]
    if points >= 1000:
        return ranks[1]
    if points >= 100:
        return rank[2]
    if points >= 10:
        return ranks[3]
    if points >= 1:
        return ranks[4]
    if points >= 0:
        return ranks[5]