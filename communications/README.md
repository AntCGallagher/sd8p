# Communications

## Usage
To run the communications system, make sure the RF stick is plugged in and run the following from the main directory (ex. `/sd8p/`):
```
python communications/communications.py
```

The PC sends messages to the Arduino, and receives OK and ERR messages indicating whether a message was successfully sent.

## Arduino Message Policy
The Arduino has a counter for message IDs that iterates every time a message is stored. Thus, when a message is received we have 3 different possibilities for the message ID.
```
if (message_id == counter)
	// The next expected message has been received
	store message
	reply OK + counter
else if (message_id < counter)
	// We have already received this message, so the OK message might have been lost
	ignore message
	reply OK + counter
else if (message_id > counter) 
	// The message isn't the next expected instruction, so we must have lost some messages inbetween
	ignore message 
	reply ERR + counter

```

## PC Message Policy
The PC receives commands from the strategy system and loads them into a Queue to be sent. It then sends them over the serial with an ID, and awaits a response. Similarly, it keeps track of the ID of the message at the head of the Queue, and only removes it when it's certain the message has been received.
```
if (ok_message) 
	// Delete all messages up to the given ID
	remove messages m : Queue where (m.id <= ok_message.id)
else if (err_message)
	// Resend all messages up to the given ID
	resend messages m : Queue where (m.id <= err_message.id)
else
	// Check if any of the messages have timed out, and if so resend
	resend messages m : Queue where (m.timeout > time.now)
```
