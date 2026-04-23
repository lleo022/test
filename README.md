# E1A Malware Lab Final Project Skeleton
### by Alec, Savannah, Anthony, Andrew

## Project Structure

```
project-skeleton
├── client
│   ├── app.py
│   └── cybersploit_client
│       ├── actions
│       ├── commands
│       └── util
├── payload
│   └── server.py
```

"Client" is the command and control for our toy malware. This is what
the attacker will run on their machine. This client will give a nice
cli to the user to run commands. Fill out the _commands_ folder, using
the existing 2 commands as an example to create new commands! The _actions_
and _util_ folders are provided just in case you would like to use that
structure - keep them or delete them as you'd like!


"Server" is the part of our malware that is actually deployed on the
victim. It consists of a basic TCP server that accepts connections on
port 5050. 

All python files are heavily commented to help describe what is going on,
what needs to be changed, and what should not be changed.
