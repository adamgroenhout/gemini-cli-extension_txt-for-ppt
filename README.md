# Gemini CLI Extension

This extension provides a command to convert any text input into the plain text format required by Microsoft PowerPoint for importing slides.

## Features

- **Intelligent Summarization**: Analyzes input text and synthesizes it into concise, impact-oriented bullet points suitable for presentation slides.
- **Strict Formatting**: Ensures output adheres to PowerPoint's specific import requirements:
    - Zero indentation for Slide Titles (Title Case).
    - Single tab (`\t`) for Main Bullet points.
    - Multiple tabs for Sub-points.
    - Windows-style Line Endings (`\r\n`).
- **Clean Output**: Guarantees raw text output without Markdown formatting or conversational filler.
