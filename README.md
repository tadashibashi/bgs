# Brokeman's Game Station
![Landing Page Mockup](readme/bgs-landing-page-mockup.png)


## We're Live! 🚀

Play and share your game creations [here](https://brokemans-gamestation-903d50ec6ce7.herokuapp.com/)!


## Tools

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)


## Featured Games
![Game Display](readme/bgs-games-index.png)

## Play Games in Dark & Light Mode
![Light & Dark Mode](readme/bgs-colormode.png)

## Search for Games 
![Search Bar Functions](readme/bgs-searchbar-games.png)

## Create and Edit Reviews
![Comments Display](readme/bgs-comments.png)

## An Early Wireframe
![Early Wireframe](readme/bgs-early-wireframe.png)

## Code Preview

This is an example of using Bootstrap 5's modals to edit comments / reviews

The script at the bottom forwards a button click to another form to confirm the deletion of a comment.

```html django templating langauge
<div class="modal fade" id="edit-modal" tabindex="-1" role="dialog">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <form action="" method="post" id="edit-form">
                {% csrf_token %}
                <div class="modal-header">
                    <h5 class="modal-title" id="edit-title">
                        Edit Comment
                    </h5>
                    <button type="button" class="btn close" data-bs-dismiss="modal" aria-label="Close">
                        <i class="bi bi-x-lg"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <label for="edit-text" class="form-label">Content:</label>
                    <textarea id="edit-text" class="form-control mb-4" name="content" rows="10"></textarea>
                    <label for="edit-rating" class="form-label">Rating: </label>
                    <select id="edit-rating" class="form-control" type="number" name="rating">
                        <option value="5">★★★★★</option>
                        <option value="4">★★★★</option>
                        <option value="3">★★★</option>
                        <option value="2">★★</option>
                        <option value="1">★</option>
                        <option value="0">No Rating</option>
                    </select>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-outline-danger position-absolute start-0 bottom-0 mb-3 ms-3" id="delete-review-form-submit-delegate" type="button">Delete</button>
                    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-success">Submit</button>
                </div>
            </form>
            <form id="delete-review-form" action="" method="POST">
                {% csrf_token %}
                <input type="submit" id="delete-review-form-submit" hidden>
            </form>
        </div>
    </div>
</div>

<script>
    window.addEventListener("load", evt => {
        const deleteFormSubmitEl = document.getElementById("delete-review-form-submit");
        const deleteFormSubmitDelegateEl = document.getElementById("delete-review-form-submit-delegate");

        deleteFormSubmitDelegateEl.addEventListener("click", evt => {
            deleteFormSubmitEl.click();
        });
    });
</script>
```

## Icebox Features

- Enable replies to comments/reviews
- Host games on AmazonS3
- Email verification and admin approval for game uploads
- Antivirus to prevent malicious malware uploads


Please check out our [Trello](https://trello.com/b/N7TDLKGa/brokemans-game-station) for more info!


## Interested in contributing to our project?

## Getting Started

### Requirements:

- Python version 3.11+

- Python libraries:
  - boto3
  - Django
  - django-environ
  - psycopg2
  - requests


First, clone the repository.

Next, you will need to create a .env file at `bgs/.env` containing the following:

| Key                   | Description                                                                                                     |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| SECRET_KEY            | Arbitrary string for Django hashing & cryptographic signing.                                                    |
| DEBUG                 | "True": Debug mode "False": Production                                                                          |
| DB_NAME               | Name for main postgresql database. Locally hosted for now. Make sure to create this db prior to running server. |
| PORT                  | Server port number. Left unspecified, it will default to 3000.                                                  |
| DB_PASSWORD           | Password for PostgreSQL database                                                                                |
| DB_USER               | Username for PostgreSQL database                                                                                |                                   
| DB_HOST_LOCAL         | Host name for local testing branch of the database. Most likely: localhost                                      |
| DB_HOST_DEBUG         | Host name for the testing branch of the database                                                                |
| DB_HOST_DEPLOY        | Host name for the deployment branch of the database                                                             |
| AWS_ACCESS_KEY_ID     | AWS access key id credential                                                                                    |
| AWS_SECRET_ACCESS_KEY | AWS secret access key credential                                                                                |
| S3_BUCKET             | Name of the S3 bucket                                                                                           |
| S3_BASE_URL           | Regional URL location where bucket is hosted                                                                    |

Migrate database changes to your local database
```shell
python3 manage.py migrate
```

Run server
```shell
python3 manage.py runserver
```

Optional: Use `do` script shortcut to run commands. Unix-only.
- Make `do` script executable `chmod +x ./do`
- Run python manage.py commands `./do <command>`

Optional: Make `crudhelper` executable using the same command as with `do`
- This script allows you to access the Python shell with all Models preloaded