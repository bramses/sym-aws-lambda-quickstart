# Sym Lambda Krabby Patty Recipe

### [handler.py](/modules/my-lambda/handler.py)

The `handle` function handles `escalation` and `de-escalation`. 
It returns a formulaic response based on user input in the approval workflow.
This response is returned from the triggered lambda, and can be seen in `CloudWatch`.

### [impl.py](/modules/impl.py)

![pic of the top-secret channel](/docs/top-secret.png)

Uses an `after_approve` hook to test against the payload. If there is a match (password: 'Every. Villain. Is. Lemons.' && options: 'I am Spongebob'), you'll see the Krabby Patty recipe in the `top-secret` channel!