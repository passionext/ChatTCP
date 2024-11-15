
from InquirerPy import inquirer

fav_lang = inquirer.select(
    message = "What's your favorite language:",
    choices = ["Go", "Kotlin", "Python", "Rust", "Java", "JavaScript"])
