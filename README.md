# Backend Practical
Using Django, create a simple API that allows users to post and retrieve their reviews.
Acceptance Criteria
* The completed assignment must be hosted in a git repository
    * The repository must include commit history (e.g., more than one commit)
* Users are able to submit reviews to the API
* Users are able to retrieve reviews that they submitted
* Users cannot see reviews submitted by other users
* Use of the API requires a unique auth token for each user
* Submitted reviews must include, at least, the following attributes:
    * Rating - must be between 1 - 5
    * Title - no more than 64 chars
    * Summary - no more than 10k chars
    * IP Address - IP of the review submitter
    * Submission date - the date the review was submitted
    * Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether
    * Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether
* Unit tests must be included providing 100% code coverage
Optional:
* Provide an authenticated admin view that allows me to view review submissions
* Document the API
Organize the schema and data models in whatever manner you think makes the most sense and feel free to add any additional style and flair to the project that you'd like.

# Reviews API
The Reviews API can be accessed by issuing a POST request to the documented endpoints. Each request must, at a minimum, be sent with a field entitled "api_key". Information about how to create API keys is documented below in Administrator's interface. In addition to providing an API key, the user must be logged in through Django's default authentication system. This provides Django with user information, while the API key proves the user has been given authorization to use the API.

## /api/postReview/
Submits a review to the API. Must contain the following fields:
* **title** Title of the review. Can be no longer than 64 characters long.
* **company** ID number (primary key) of the Company being reviewed.
* **rating** An integer ranging from 1 to 5, inclusive
* **summary** The long-form description of the review. Can be no longer than 10000 characters long
* **api_key** the API key given to the user, indicating authorization to access the API

## /api/getReview/<review_id>/
Retrieves the review with id *review_id*, which is passed in the URL path. Users are only authorized to view reviews they themselves submitted, and only if they are logged in. Additionally, the post must contain the following field:
* **api_key** he API key given to the user, indicating authorization to access the API

If authentication and authorization is verified, the API will respond with a serialized JSON representation of the review model in the database.

## /api/getOwnReviews/
Retrieves all reviews submitted by the logged-in user. Must contain the following field:
* **api_key** he API key given to the user, indicating authorization to access the API

If authentication and authorization is verified, the API will respond with a serialized JSON representation of all the reviews submitted by the user.

# Administrator's interface
Like most Django applications, there is an administrator's interface accessible at /admin. You need to be a superuser to access it. See [Django's documentation](https://docs.djangoproject.com/en/2.0/intro/tutorial02/#creating-an-admin-user) for more information about creating admin users if you don't have one set up yet. All models are registered, allowing for a good deal of configurability on the part of the Administrator.

As mentioned above, you will need to create an API key for a user in order to allow that user to access the API. You can do this by logging in at /admin, then going to REVIEWSAPI > Api Keys. In the top-right corner, you will see a button called *Add API Key*. You can then select a user and get an API key. API keys are UUID4 format keys. A default one is provided for you, but you can enter your own if you desire.
