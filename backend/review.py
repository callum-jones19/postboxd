class Review():
    def __init__(self, film_name: str, rating: int, comment: str):
        self.film_id = film_name
        self.rating = rating
        self.comment = comment

    def get_rating(self) -> int:
        return self.rating

    def get_film(self) -> str:
        return self.film_id

    def get_comment(self) -> str:
        return self.comment
