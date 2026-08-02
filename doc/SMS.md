#### SMS for Developers

Test SMS applications without costs, phone numbers, or external dependencies. 
A complete local development tool that simulates SMS functionality with a beautiful web interface.

https://github.com/pcdkd/smsdev

## Global Installation:

# Install globally via npm
npm install -g @relay-works/sms-dev

# Start the development environment
sms-dev start

# Open in browser
# API: http://localhost:4001
# UI: http://localhost:4000

## Local Installation:

# Install locally in your project
npm install --save-dev @relay-works/sms-dev

# Add to package.json scripts
{
  "scripts": {
    "sms-dev": "sms-dev start"
  }
}

# Run in your project
npm run sms-dev

## Basic SMS Testing

```
// Your application code - raw message
const response = await fetch('http://localhost:4001/v1/messages', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    to: '+1234567890',
    body: 'Hello from my app!'
  })
})

const message = await response.json()
console.log('Message sent:', message.id)
console.log('Message text:', message.message)
```