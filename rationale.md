# Solution rationale

The solution is a simple django api that takes an input a blog post
composed of a title and some paragraphs, run them against a ML endpoint to find
foul text.
This solution will look for foul text in both the title and each of the sentences in the paragraphs.
If there is any failure while contacting the endpoint, the blogpost with the sentence due to be processed
will be saved into a specific table for offline re-processing.
Sentences that haven't been processed due to API issues will be processed on a schedule basis,
for the sake of the example every minute, and if successful removed from the backlog.


## Tech

I specifically chose Django not because the best tool for the job but merely because I am quite familiar and could
bring something quick up to speed. I decided also to use Flask for the ML endpoint as it was a simple API that really
didn't need anything more than an exposed API.


## Known limitations

There are known limitations in the solution that are the outcome of a reduced
scope which is the one of the tech test.

- The current backlog is processed via a cron in Docker, and while it works this is far from an ideal solution.
Something better would be to use a queueing system backed from Redis (e.g. Django-Q) which provide
a nice and flexible solution for async tasks. Celery would be another solution as well, but I deemed them to be
out of scope within this tech task.

- The ML endpoint has no place in the same repository as the ingestion endpoint, ideally it should sit in a different place

- Django is not the best API tool available, some others are far better placed for simple API operations
- Deleting backlog entries is an ok solution, in a real world scenario it would likely make more sense to keep track of what
and when something failed. Entries can be disabled rather than deleted

- More testing coverage would be nice
- Sentences are processed each time as new; this works for this use case but in real world applications it would make
more sense to cache these results to avoid costly re-computing. Also, this can be improved with an addition of the model version
that did the detection, and can be used to update detections in the case of a newer model and help compare models performances
in time.
- I decided to use *title* as the key for a blog post, making it unique within the database. This is not something I'd want
in a real world application as it might constrain the application too much. 
- The ingestion API does its best to do everything on the fly, but in the event of long pieces
of text to analyze, it could easily become a bottleneck. In that case it would be better to send larger texts directly
to be processed offline in order to not saturate the ingestion api.

## Conclusion

I had fun doing this, I hope you like my solution!
