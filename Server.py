from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import os
from datetime import datetime

# creating a server instance
app = Server('my-MCP_server')
os.makedirs('Test_Files', exist_ok=True)

# declaring all the available tools in the server
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name = 'create_note',
            description='Creates a new Markdown note about the Asked Questions with the given title and content.',
            inputSchema ={
                'type': 'object',
                'properties': {
                    "filename": {
                        "type": "string", 
                        "description": "Name of the file (e.g., 'python_basics')"
                    },
                    "content": {
                        "type": "string", 
                        "description": "The markdown content to write inside the file"
                    }
                },
                "required": ["filename", "content"]
                    }
            ), 
        Tool(
                name='read_note',
                description='Reads and returns the full content of an existing Markdown note by filename. Use this when the user wants to view, review, or refer back to a previously created note.',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read, without extension (e.g., 'python_basics')"
                        }
                    },
                    "required": ["filename"]
                }
            ),
        Tool(
                name='update_note',
                description='Updates the content of an existing Markdown note. Use this when the user wants to add, edit, or change information in a note that already exists. Overwrites the existing content with the new content provided.',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to update, without extension (e.g., 'python_basics')"
                        },
                        "content": {
                            "type": "string",
                            "description": "The new markdown content to overwrite the file with"
                        },
                        "append": {
                            "type": "boolean",
                            "description": "If true, adds the new content to the end of the existing note instead of replacing it. Defaults to false."
                        }
                    },
                    "required": ["filename", "content"]
                }
            ),
        Tool(
                name='delete_note',
                description='Permanently deletes an existing Markdown note by filename. Use this when the user explicitly asks to remove or delete a note. This action cannot be undone.',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to delete, without extension (e.g., 'python_basics')"
                        }
                    },
                    "required": ["filename"]
                }
            ),
        Tool(
                name='list_notes',
                description='Lists all existing Markdown notes in the notes directory. Returns filenames and their last modified dates. Use this to check what notes exist before reading, updating, or deleting one.',
                inputSchema={
                    'type': 'object',
                    'properties': {},
                    "required": []
                }
            ), 
        Tool(
            name='send_note_via_email',
            description='Sends the content of an existing Markdown note to a specified email address. '
                        'Use this when the user wants to share a note with someone via email. '
                        'Always use list_notes first if you are unsure whether the note exists.',
            inputSchema={
                'type': 'object',
                'properties': {
                    "filename": {
                        "type": "string",
                        "description": "Name of the note to send, without extension (e.g., 'python_basics')"
                    },
                    "to_email": {
                        "type": "string",
                        "description": "The recipient's email address (e.g., 'john@example.com')"
                    },
                    "subject": {
                        "type": "string",
                        "description": "The email subject line. If not provided, defaults to the note filename."
                    },
                    "body_intro": {
                        "type": "string",
                        "description": "Optional short message to include before the note content in the email body."
                    }
                },
                "required": ["filename", "to_email"]
            }
),
        
    ]

# handling the tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == 'create_note':
        filename = arguments['filename']
        content = arguments['content']
        if not filename.endswith('.md'):
            filename += '.md'
        filepath = os.path.join('Test_Files', filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return [TextContent(type='text', text=f"Note '{filename}' created successfully!")]
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to create note: {str(e)}")]
    
    if name == 'read_note':
        filename = arguments['filename']
        if not filename.endswith('.md'):
            filename += '.md'
        filepath = os.path.join('Test_Files', filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return [TextContent(type='text', text=content)]
        except FileNotFoundError:
            return [TextContent(type='text', text=f"Error: Note '{filename}' does not exist.")]
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to read note: {str(e)}")]

    if name == 'update_note':
        filename = arguments['filename']
        content = arguments['content']
        append = arguments.get('append', True)
        if not filename.endswith('.md'):
            filename += '.md'
        filepath = os.path.join('Test_Files', filename)

        if not os.path.exists(filepath):
            return[TextContent(type='text', text = f"Error: Note '{filename}' does not exist. Cannot update a non-existent note.")]
        
        mode = 'a' if append else 'w'
        try:
            with open(filepath, mode, encoding='utf-8') as f:
                if append:
                    f.write('\n' + content)  # add newline before appended content
                else:
                    f.write(content)
            action = "Appended to" if append else "Updated"
            return [TextContent(type='text', text=f"{action} note '{filename}' successfully!")]
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to update note: {str(e)}")]

    if name == 'delete_note':
        filename = arguments['filename']
        if not filename.endswith('.md'):
            filename += '.md'
        filepath = os.path.join('Test_Files', filename)

        # ✅ Fix 4 — clean message if file doesn't exist
        if not os.path.exists(filepath):
            return [TextContent(type='text', text=f"Error: Note '{filename}' does not exist.")]
        try:
            os.remove(filepath)
            return [TextContent(type='text', text=f"Note '{filename}' deleted successfully!")]
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to delete note: {str(e)}")]

    if name == 'list_notes':
        notes_dir = 'Test_Files'
        try:
            files = os.listdir(notes_dir)
            notes_info = []
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(notes_dir, file)
                    # ✅ Fix 2 — human readable timestamp
                    modified_time = datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ).strftime('%Y-%m-%d %H:%M')
                    notes_info.append(f"- {file} (Last Modified: {modified_time})")

            # ✅ Fix 1 — explicit message when empty
            if not notes_info:
                return [TextContent(type='text', text="No notes found in Test_Files directory.")]
            return [TextContent(type='text', text="Available notes:\n" + "\n".join(notes_info))]
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to list notes: {str(e)}")]

    if name == 'send_note_via_email':
        filename   = arguments['filename']
        to_email   = arguments['to_email']
        subject    = arguments.get('subject', None)
        body_intro = arguments.get('body_intro', '')

        # --- Build the filepath ---
        if not filename.endswith('.md'):
            filename += '.md'
        filepath = os.path.join('Test_Files', filename)

        # --- Check the note exists ---
        if not os.path.exists(filepath):
            return [TextContent(type='text', text=f"Error: Note '{filename}' does not exist. Use list_notes to see available notes.")]

        # --- Read the note content ---
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                note_content = f.read()
        except Exception as e:
            return [TextContent(type='text', text=f"Failed to read note for email: {str(e)}")]

        # --- Build the email ---
        subject    = subject or f"Note: {filename}"
        email_body = f"{body_intro}\n\n{note_content}".strip() if body_intro else note_content

        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            # --- Load credentials from environment ---
            sender_email    = os.getenv("EMAIL_ADDRESS")
            sender_password = os.getenv("EMAIL_PASSWORD")
            smtp_host       = os.getenv("SMTP_HOST", "smtp.gmail.com")
            smtp_port       = int(os.getenv("SMTP_PORT", "587"))

            if not sender_email or not sender_password:
                return [TextContent(type='text', text="Error: EMAIL_ADDRESS and EMAIL_PASSWORD must be set in your .env file.")]

            # --- Compose the message ---
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = sender_email
            msg["To"]      = to_email

            # Plain text part (the raw markdown)
            msg.attach(MIMEText(email_body, "plain"))

            # --- Send it ---
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()                               # encrypt the connection
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())

            return [TextContent(type='text', text=f"Note '{filename}' sent successfully to {to_email}!")]

        except smtplib.SMTPAuthenticationError:
            return [TextContent(type='text', text="Error: Email authentication failed. Check your EMAIL_ADDRESS and EMAIL_PASSWORD in .env.")]
        except smtplib.SMTPException as e:
            return [TextContent(type='text', text=f"Email sending failed: {str(e)}")]
        except Exception as e:
            return [TextContent(type='text', text=f"Unexpected error sending email: {str(e)}")]
    
    raise ValueError(f"Unknown tool: {name}")


# running the server
if __name__ == "__main__":
    import asyncio

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(main())













