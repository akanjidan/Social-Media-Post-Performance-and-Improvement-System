import typer


app = typer.Typer()



@app.command()
def DisplayPost(post: str):
    print(f"{post}")

#For counting the number of hashtags
@app.command()
def hashtagcount(post: str):
    """
     Count the number of hashtags in the given text.
     Args:
     text (str): The input text containing hashtags.
     Returns:
     int: The number of hashtags in the text.
     """
    # Split the text into words
    words = post.split()
    # Count the words that start with '#'
    hashtag_count = sum(1 for word in words if word.startswith('#'))
    print(hashtag_count)
    return hashtag_count


@app.command()
def postlength(post: str):
    """
    Calculate the length of a post.

    Args:
    post (str): The input text of the post.

    Returns:
    int: The length of the post in characters.
    """
    print(len(post))
    return len(post)


@app.command()
def tone(post: str):
    print(f"{post}")

@app.command()
def message(post: str):
    print(f"{post}")

@app.command()
def narrative(post: str):
    print(f"{post}")

@app.command()
def hashtageffec(post: str):
    print(f"{post}")

@app.command()
def controversial(post: str):
    print(f"{post}")

@app.command()
def cta(post: str):
    print(f"{post}")

@app.command()
def engagenment(post: str):
    print(f"{post}")

@app.command()
def suggestion(post: str):
    #paste code here
    print(f"{post}")


if __name__ == "__main__":
    app()