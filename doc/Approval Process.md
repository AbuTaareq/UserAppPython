# Approval Process by ChatGPT

A typical flow looks like this:

## 1. Agent creates request
Agent Alice assigns User Bob.

Backend creates a record:
```sql
agent_assignment_request

request_id
user_id
agent_id
token
expires_at
status
```

Example:

```text
request_id = 123
token = 6c3a4f8e-3db8-4b7d-8a51-xxxxx
status = PENDING
```

---

## 2. Email contains link

```html
<a href="https://app.example.com/agent-request/6c3a4f8e-3db8-4b7d-8a51-xxxxx">
    Review Request
</a>
```

---

## 3. React Route

```tsx
<Route
    path="/agent-request/:token"
    element={<AgentApprovalPage />}
/>
```

When user clicks the email link:

```text
https://app.example.com/agent-request/6c3a4f8e-3db8-4b7d-8a51-xxxxx
```

React loads:

```tsx
AgentApprovalPage
```

---

## 4. Read token from URL

```tsx
import { useParams } from "react-router-dom";

export default function AgentApprovalPage() {

    const { token } = useParams();

    console.log(token);

    return <></>;
}
```

Result:

```text
6c3a4f8e-3db8-4b7d-8a51-xxxxx
```

---

## 5. Ask backend if token is valid

When page loads:

```tsx
useEffect(() => {

    const load = async () => {

        const response = await api.get(
            `/agent-request/${token}`
        );

        setData(response.data);
    };

    load();

}, [token]);
```

FastAPI:

```python
@router.get("/agent-request/{token}")
async def get_request(token: str):

    request = await db.fetchrow(
        """
        select *
        from agent_assignment_request
        where token = $1
        and status = 'PENDING'
        and expires_at > now()
        """,
        token
    )

    if not request:
        raise HTTPException(404)

    return request
```

---

## 6. Show Approval Screen

```text
Agent Alice would like to become your assigned agent.

[ Approve ]
[ Deny ]
```

---

## 7. User clicks Approve

React:

```tsx
await api.post(
    `/agent-request/${token}/approve`
);
```

FastAPI:

```python
@router.post("/agent-request/{token}/approve")
async def approve_request(token: str):

    # verify token

    # assign user to agent

    # mark request approved

    return {"success": True}
```

---

## The Security Improvement

I would actually recommend NOT putting the token in the path.

Instead:

```text
https://app.example.com/agent-request?token=abc123
```

Then:

```tsx
const [searchParams] = useSearchParams();

const token = searchParams.get("token");
```

or even better:

```text
https://app.example.com/agent-request?request=123&sig=xyz
```

where `sig` is a cryptographically signed value.

---

## What I Would Do

Since you're already using JWT authentication, I would build it like this:

### Anonymous user clicks email

```text
/app/agent-request?token=abc123
```

React:

1. Extract token.
2. Call FastAPI.
3. Backend validates token.

If user is not logged in:

```text
Please login to continue.
```

Store the token temporarily.

After login:

```text
Agent Alice requests assignment.

[Approve]
[Deny]
```

This gives you:

- Secure approval
- Audit trail
- Expiring links
- Works from email
- Uses your existing JWT authentication

That's very close to how enterprise systems typically implement email-based approvals.
